from gurobipy import Model, GRB, quicksum
from itertools import product
import numpy as np
import pandas as pd
import pickle
import time
from elasticsearch import Elasticsearch
import os
import folium

def W_matrix(password_elasticsearch):
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
        m[m == 0.35] = 0
        # store demand matrix for each district in dictionary
        W[district] = m

    # store W matrix with pickle
    pickle.dump(W, open("pickles/W_matrix.p", "wb"))

    # print time
    toc = time.time()
    elapsed_time = toc - tic
    print('Total running time of creating W matrix: {:.2f} seconds'.format(elapsed_time))


def optimization_model(password_elasticsearch):
    """sth.."""

    m = Model("Locker optimization")

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

    for district in districts:
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
            print("%s  %g" % (v.varName, v.x))
            if "y" in v.Varname:
                y.append(v.x)
            elif "X" in v.Varname:
                x.append(v.x)
        print("Obj: %g" % m.objVal)

    # todo: store data, in dict?

        # todo: change location to new function
        index = [i for i, j in enumerate(y) if j == 1]
        x = locations[["lats", "longs"]].iloc[index]
        m = folium.Map(location=[(min(x["lats"]) + max(x["lats"])) / 2, (min(x["longs"])+ max(x["longs"])) / 2], zoom_start=12)

        for lat, long in zip(x["lats"], x["longs"]):
            folium.CircleMarker(location=(lat, long), radius=2).add_to(m)

        m.save("outputs/pickup_points.html")

if __name__ == '__main__':
    optimization_model(password_elasticsearch=".")
