import pickle
from gurobipy import Model, GRB, quicksum
from itertools import product
import time
import pandas as pd
import folium

def optimizing_locker_network_bonus(districts: list, P: float, capacities: list, costs: dict, W: dict, Demand, max_percentage: float, sensitivity_analysis=None):
    """optimizes the model for each district in the provided list, for inputs P, C, W and demand"""
    tic = time.time()

    # transform demand to correct format
    D = {}
    for district in districts:
        # for all demands where district in demand dataframe is equal to a district from the loop
        # store in dictionary under district key as numpy array
        D[district] = Demand.loc[Demand["key"].str[0:4] == district]["avg_daily_location"].to_numpy()

    # empty dictionary to store results for each district
    results = {}

    for district in districts:
        # initiate gurobi model
        m = Model("Locker optimization")

        n = len(D[district])
        ij = list(product(range(n), range(n)))

        # add the (decision) variables
        # now capacities also added to y and X
        y = m.addVars(n, capacities, vtype=GRB.BINARY, name="y")
        X = m.addVars(ij, capacities, vtype=GRB.BINARY, name="X")

        # add formula 2(constraint) from the model
        for i in range(n):
            m.addConstr(quicksum(X[i, j, k] for j in range(n) for k in capacities) <= 1)

        # add formula 3(constraint) from the model
        for j in range(n):
            for k in capacities:
                m.addConstr(quicksum(D[district][i] * W[district][i, j] * X[i, j, k] for i in range(n)) <= k * y[j, k])

        # add formula 4(constraint) from the model
        m.addConstr(quicksum(D[district][i] * W[district][i, j] * X[i, j, k] for i in range(n) for j in range(n) for k in capacities) >= P * quicksum(D[district][i] for i in range(n)))

        # add formula 5(constraint) from the model
        m.addConstrs(X[i, j, k] <= y[j, k] for i in range(n) for j in range(n) for k in capacities)

        # add formula 6(constraint) from the model
        for i in range(n):
            for j in range(n):
                for k in capacities:
                    if W[district][i, j] == 0:
                        m.addConstr(X[i, j, k] == 0)

        # additional constraint that ensures that only one locker can be located at node j:
        m.addConstrs(quicksum(y[j, k] for k in capacities) <= 1 for j in range(n))

        # formula 1(objective function) from the model
        obj = quicksum(y[j, k] * costs[k] for j in range(n) for k in capacities)
        m.setObjective(obj, GRB.MINIMIZE)

        # todo: remove
        #m.Params.MIPFocus = 1
        # m.Params.Cuts = 3
        # m.Params.MIPGap = 0.05  # 5%
        # m.Params.TimeLimit = 300  # 5 minutes

        # optimize the defined objective function with the constraint
        m.optimize()
        # m.write("model.lp")

        # create empty lists and dictionary to store the results
        y = {}
        x = []

        try:
            # print the result of the objective function
            print("Obj: %g" % m.objVal)

            # store the results
            for v in m.getVars():
                if "y" in v.Varname and v.X == 1:
                    # store the index as key and locker size as value in right format, when y==1
                    y[int(v.Varname.split(",")[0][2:])] = int(v.Varname.split(",")[1][:-1])
                elif "X" in v.Varname and v.X == 1:
                    # appends a list with the indices of start and end node when x==1
                    ind = [int(v.Varname.split(",")[0][2:]), int(v.Varname.split(",")[1])]
                    x.append(ind)
        except AttributeError:      # captures error when model is infeasible. Useful for sensitivity analysis
            pass

        # store the results in a dictionary under the key district
        results[district] = [x, y]

    pickle.dump(results, open("pickles/results_bonus.p", "wb"))

    # print total time for optimizing the model for all the districts
    toc = time.time()
    elapsed_time = toc - tic
    print('Total running time of optimizing network: {:.2f} seconds'.format(elapsed_time))


def plot_network_bonus(results: dict, districts: list):
    # load locations data
    locations = pd.read_pickle("pickles/assignment_geo_coords.p")

    coords = {}
    # for each district store in a dictionary all the latitude and longitude data of the locations in that district
    # important to do it per district, since the results stored the indexes also per district
    for district in districts:
        coords[district] = locations[locations["postcode"].str[:4] == district][["lats", "longs"]].to_dict('list')

    # initiate map
    m = folium.Map(location=[(min(locations["lats"]) + max(locations["lats"])) / 2, (min(locations["longs"]) +
                                                                                     max(locations["longs"])) / 2],
                   zoom_start=13)
    # add custom map tile
    folium.TileLayer(
        tiles='https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
    ).add_to(m)

    # initiate dictionary with where different locker sizes are linked to colours
    colours = {6: "blue", 12: "red", 18: "green"}

    # for each district, plot a marker for each storage location(y=1), a circle marker for each location and a line from
    # each location to the storage location
    for district in districts:
        for i in results[district][1].keys():  # results[district][1].keys() stores the indices where y=1 for each district
            folium.Marker(location=(coords[district]["lats"][i], coords[district]["longs"][i]),
                          icon=folium.Icon(color=colours[results[district][1][i]], icon="inbox"),
                          popup="Locker in district " + district + " with locker size: " + str(results[district][1][i])).add_to(m)

        for j in results[district][0]:  # results[district][0] stores a list of the indices where x=1
            folium.CircleMarker(location=(coords[district]["lats"][j[0]], coords[district]["longs"][j[0]]), radius=1,
                                color="white", popup="Location in district " + district).add_to(m)
            folium.PolyLine([(coords[district]["lats"][j[0]], coords[district]["longs"][j[0]]),
                             (coords[district]["lats"][j[1]], coords[district]["longs"][j[1]])], color="grey",
                            opacity=0.5).add_to(m)
    m.save("outputs/locker_network_bonus.html")


