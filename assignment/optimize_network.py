from gurobipy import Model, GRB, quicksum
from itertools import product
import numpy as np
import pandas as pd
import pickle
import time
from elasticsearch import Elasticsearch
import os
import folium
import matplotlib.pyplot as plt


def W_matrix(password_elasticsearch: str, districts: list):
    """creates W_matrix as a dictionary of numpy arrays using elasticsearch, where the keys are the districts as
    provided in the districts list"""

    # starts timer
    tic = time.time()

    # connect to elasticsearch
    es = Elasticsearch(hosts="http://elastic:" + password_elasticsearch + "@localhost:9200")

    # load locations dataframe
    locations = pd.read_pickle("pickles/assignment_geo_coords.p")
    # create lists with all locations
    locations_unique = locations["postcode"].to_list()
    # create and empty dictionary to store the W matrix
    W = {}

    for district in districts:
        i = 0
        for locations in locations_unique:
            # for each district and each location check if location is in district
            if locations[:4] == district:
                # if location is in district
                # query all items with start_point_travel == location and end_point_travel in district
                search_body = {
                                "query": {
                                    "bool": {
                                        "must": [
                                            {"wildcard": {"end_point_travel.keyword": locations[:4] + "*"}},
                                            {"term": {"start_point_travel.keyword": locations}}
                                        ]
                                    }
                                }
                            }
                data = es.search(index="assignment_distances", body=search_body, size=1000)
                # retrieve relevant data and store in numpy array
                output = np.array([data["hits"]["hits"][i]["_source"]["travel_time_on_bike_in_seconds"] for i in range(len(data["hits"]["hits"]))])
                # insert 0 at index i to get 0s on diagonals
                output = np.insert(output, i, 0)

                if i > 0:   # if matrix m is not empty, stack output on matrix m
                    m = np.vstack([m, output])
                if i == 0:  # if matrix m is empty, set m equal to queried output
                    m = output
                i += 1

        # calculated demand using travel time from matrix m
        m = 0.35 - (0.05 / 60 * m)      # todo: as inputs?
        # set all items with zero travel time to zero demand
        m[m == 0.35] = 0        # todo: delete this part?
        # store demand matrix for each district in dictionary
        W[district] = m

    # store W matrix with pickle
    pickle.dump(W, open("pickles/W_matrix.p", "wb"))

    # print time
    toc = time.time()
    elapsed_time = toc - tic
    print('Total running time of creating W matrix: {:.2f} seconds'.format(elapsed_time))


def optimization_model(districts: list, P: float, C: float, W: dict, Demand):
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
        y = m.addVars(n, vtype=GRB.BINARY, name="y")
        X = m.addVars(ij, vtype=GRB.BINARY, name="X")

        # todo: check model
        # add formula 2(constraint) from the model
        for i in range(n):
            m.addConstr(quicksum(X[i, j] for j in range(n)) <= 1)

        # add formula 3(constraint) from the model
        for j in range(n):
            m.addConstr(quicksum(D[district][i] * W[district][i, j] * X[i, j] for i in range(n)) <= C * y[j])

        # add formula 4(constraint) from the model
        m.addConstr(quicksum(D[district][i] * W[district][i, j] * X[i, j] for i in range(n) for j in range(n)) >= P * quicksum(D[district][i] for i in range(n)))

        # add formula 5(constraint) from the model
        m.addConstrs(X[i, j] <= y[j] for i in range(n) for j in range(n))

        # add formula 6(constraint) from the model
        for i in range(n):
            for j in range(n):
                if W[district][i, j] == 0:
                    m.addConstr(X[i, j] == 0)

        # formula 1(objective function) from the model
        m.setObjective(quicksum(y[j] for j in range(n)), GRB.MINIMIZE)      # formula 1 - objective function
        # optimize the defined objective function with the constraint
        m.optimize()

        # print the result of the objective function
        print("Obj: %g" % m.objVal)

        # create empty lists to store the results
        y = []
        x = []
        for v in m.getVars():
            if "y" in v.Varname and v.X == 1:
                # appends the index of where y==1
                y.append(int(v.Varname[2:-1]))
            elif "X" in v.Varname and v.X == 1:
                # appends a list with the index of start and end node when x==1
                ind = str(v.Varname[2:-1]).split(",")
                # get the indices from string to integer
                ind = list(map(int, ind))
                x.append(ind)

        # store the results in a dictionary under the key district
        results[district] = [x, y]

    # store using pickle
    pickle.dump(results, open("pickles/results.p", "wb"))

    # print total time for optimizing the model for all the districts
    toc = time.time()
    elapsed_time = toc - tic
    print('Total running time of optimizing network: {:.2f} seconds'.format(elapsed_time))


def plot_results(results: dict, districts: list):
    """plots the nodes used as storage location and the arcs to the storage location using folium, and plots the total
    number of storage location per district as a bar graph """

    # load dataframe with all locations
    locations = pd.read_pickle("pickles/assignment_geo_coords.p")

    # initiate map
    m = folium.Map(location=[(min(locations["lats"]) + max(locations["lats"])) / 2, (min(locations["longs"]) +
                                max(locations["longs"])) / 2], zoom_start=12)


    coords = {}
    # for each district store in a dictionary all the latitude and longitude data of the locations in that district
    # important to do it per district, since the results stored the indexes also per district
    for district in districts:
        coords[district] = locations[locations["postcode"].str[:4] == district][["lats", "longs"]].to_dict('list')

    # todo: add some info to marker and colours, size etc
    # for each district, plot a marker for each storage location(y=1), a circle marker for each location and a line from
    # each location to the storage location
    for district in districts:
        for i in results[district][1]:      # results[district][1] stores the indices where y=1 for each district
            folium.Marker(location=(coords[district]["lats"][i], coords[district]["longs"][i])).add_to(m)

        for j in results[district][0]:      # results[district][o] stores a list of the indices where x=1
            folium.CircleMarker(location=(coords[district]["lats"][j[0]], coords[district]["longs"][j[0]]), radius=1).add_to(m)
            folium.PolyLine([(coords[district]["lats"][j[0]], coords[district]["longs"][j[0]]), (coords[district]["lats"][j[1]], coords[district]["longs"][j[1]])]).add_to(m)
    m.save("outputs/pickup_points.html")

    count = []
    for district in districts:
        # count the length of the list with indices where y=1
        count.append(len(results[district][1]))
    # todo: layout
    plt.xticks(rotation='vertical')
    plt.bar(districts, count)
    plt.savefig("outputs/bar_plot_count_lockers.png")

    plt.show()

if __name__ == '__main__':
    # optimization_model(password_elasticsearch=".")
    plot_results()
