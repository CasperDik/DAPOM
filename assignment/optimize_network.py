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


def W_matrix(password_elasticsearch: str):
    tic = time.time()

    # connect to elasticsearch
    es = Elasticsearch(hosts="http://elastic:" + password_elasticsearch + "@localhost:9200")

    # load dataframe with all locations # todo: load pickle
    locations = pd.read_csv("input_data/geo_coordinates_per_each_location_cleaned.csv")
    # create lists with all locations and all districts
    districts = locations["postcode"].str[:4].drop_duplicates().to_list()
    locations_unique = locations["postcode"].to_list()
    # create and empty dictionary
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
                if i > 0:   # if matrix m has a row, stack matrix and new row
                    m = np.vstack([m, output])
                if i == 0:  # if matrix m not created yet, set m equal to queried output
                    m = output
                i += 1
        # calculated demand using travel time from matrix m
        m = 0.35 - (0.05 / 60 * m)
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


def optimization_model(password_elasticsearch: str):
    """sth.."""
    tic = time.time()

    # load dataframe with all locations # todo: use pickle
    locations = pd.read_csv("input_data/geo_coordinates_per_each_location_cleaned.csv")
    # create lists with all locations and all districts
    districts = locations["postcode"].str[:4].drop_duplicates().to_list()

    # load W matrix
    if os.path.isfile("pickles/W_matrix.p"):
        W = pickle.load(open("pickles/W_matrix.p", "rb"))
    else:
        W_matrix(password_elasticsearch)
        W = pickle.load(open("pickles/W_matrix.p", "rb"))

    # load demand
    if os.path.isfile("pickles/daily_deliveries_location.p"):
        df = pd.read_pickle("pickles/daily_deliveries_location.p")
        D = {}
        for district in districts:
            D[district] = df.loc[df["key"].str[0:4] == district]["avg_daily_location"].to_numpy()
    else:
        raise SystemExit("D file does not exist")

    P = 0.25
    C = 24

    results = {}

    for district in districts:
        m = Model("Locker optimization")

        n = len(D[district])

        # decision variable
        y = m.addVars(n, vtype=GRB.BINARY, name="y")

        ij = list(product(range(n), range(n)))
        X = m.addVars(ij, vtype=GRB.BINARY, name="X")

        # formula 2
        for i in range(n):
            m.addConstr(quicksum(X[i, j] for j in range(n)) <= 1)

        # formula 3
        for j in range(n):
            m.addConstr(quicksum(D[district][i] * W[district][i, j] * X[i, j] for i in range(n)) <= C * y[j])

        # formula 4
        m.addConstr(quicksum(D[district][i] * W[district][i, j] * X[i, j] for i in range(n) for j in range(n)) >= P * quicksum(D[district][i] for i in range(n)))

        # formula 5
        m.addConstrs(X[i, j] <= y[j] for i in range(n) for j in range(n))

        # formula 6
        for i in range(n):
            for j in range(n):
                if W[district][i, j] == 0:
                    m.addConstr(X[i, j] == 0)

        # set objetive and optimize
        m.setObjective(quicksum(y[j] for j in range(n)), GRB.MINIMIZE)      # formula 1 - objective function
        m.optimize()

        y = []
        x = []
        for v in m.getVars():
            if "y" in v.Varname and v.X == 1:
                # appends the index of where y==1
                y.append(int(v.Varname[2:-1]))
            elif "X" in v.Varname and v.X == 1:
                # appends a list with the index of start and end node when x==1
                ind = str(v.Varname[2:-1]).split(",")
                # to int
                ind = list(map(int, ind))
                x.append(ind)
        print("Obj: %g" % m.objVal)

        results[district] = [x, y]

    pickle.dump(results, open("pickles/results.p", "wb"))

    toc = time.time()
    elapsed_time = toc - tic
    print('Total running time of optimizing network: {:.2f} seconds'.format(elapsed_time))


def plot_results():
    results = pickle.load(open("pickles/results.p", "rb"))

    # load dataframe with all locations # todo: use pickle
    locations = pd.read_csv("input_data/geo_coordinates_per_each_location_cleaned.csv")
    # create lists with all locations and all districts
    districts = locations["postcode"].str[:4].drop_duplicates().to_list()

    # initiate map
    m = folium.Map(location=[(min(locations["lats"]) + max(locations["lats"])) / 2, (min(locations["longs"]) +
                                max(locations["longs"])) / 2], zoom_start=12)

    coords = {}
    for district in districts:
        coords[district] = locations[locations["postcode"].str[:4] == district][["lats", "longs"]].to_dict('list')

    # todo: add some info to marker and colours, size etc
    for district in districts:
        for i in results[district][1]:
            folium.Marker(location=(coords[district]["lats"][i], coords[district]["longs"][i])).add_to(m)

        for j in results[district][0]:
            folium.CircleMarker(location=(coords[district]["lats"][j[0]], coords[district]["longs"][j[0]]), radius=1).add_to(m)
            folium.PolyLine([(coords[district]["lats"][j[0]], coords[district]["longs"][j[0]]), (coords[district]["lats"][j[1]], coords[district]["longs"][j[1]])]).add_to(m)


    m.save("outputs/pickup_points.html")

    # todo: --> Plot the number of pickup points in each district on a bar chart.
    count = []
    for district in districts:
        count.append(len(results[district][1]))

    plt.xticks(rotation='vertical')
    plt.bar(districts, count)
    plt.savefig("outputs/bar_plot_count_lockers.png")

    #plt.show()

if __name__ == '__main__':
    # optimization_model(password_elasticsearch=".")
    plot_results()
