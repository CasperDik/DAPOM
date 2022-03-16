from gurobipy import Model, GRB, quicksum
from itertools import product
import numpy as np
import pandas as pd


def demand():
    """sth.."""
    # todo: make better solution --> check recordings

    # todo: import actual travel times
    df = pd.read_excel("mock_data_weights.xlsx").to_numpy()

    # count elements equal to element [0][0] --> basically counting duplicates
    # counts all items equal in entire array thus double counting --> 9403RS - 9403RS & 9403RS - 9403RS-->both in array
    # use for the size of the matrix --> size is number of duplicates + 1
    # todo: check if these comments make sense?
    n = int(np.count_nonzero(df == df[0][0])/2+1)

    W = np.zeros((n, n))
    c = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                W[i, j] = 0.35 - 0.05/60 * df[c, 2]     # todo: make this as variables
                c += 1

    # diagonals should be 0
    # use numpy arrays
    # need index for all postcodes
    # if i==j --> 0,  if i =/= j --> insert travel time between i,j at location i,j in array
    # from postcode i to postcode j --> insert traval time

    # 0.35 - 0.05 / 60 * travel_time_on_bike_in_seconds from w --> apply this as a function to W

    # todo: how to get back to postcodes

    return W, n

def optimization_model():
    """sth.."""
    m = Model("Locker optimization")


    W, n = demand()
    D = np.random.rand(n*5)     # todo: import D
    P = 0.25
    C = 24

    # decision variable
    y = m.addVars(n, vtype=GRB.BINARY, name="y")

    ij = list(product(range(n), range(n)))
    X = m.addVars(ij, vtype=GRB.BINARY, name="X")

    # formula 2
    for i in range(n):
        m.addConstr(quicksum(X[i, j] for j in range(n)) <= 1)

    # formula 3
    for j in range(n):
        m.addConstr(quicksum(D[i] * W[i, j] * X[i, j] for i in range(n)) <= C * y[j])

    # formula 4
    m.addConstr(quicksum(D[i] * W[i, j] * X[i, j] for i in range(n) for j in range(n)) >= P * quicksum(D[i] for i in range(n)))

    # formula 5
    m.addConstrs(X[i, j] <= y[j] for i in range(n) for j in range(n))

    # formula 6
    for i in range(n):
        for j in range(n):
            if W[i, j] == 0:
                m.addConstr(X[i, j] == 0)

    # set objetive and optimize
    m.setObjective(quicksum(y[j] for j in range(n)), GRB.MINIMIZE)      # formula 1
    m.optimize()

    for v in m.getVars():
        print("%s  %g" % (v.varName, v.x))
    print("Obj: %g" % m.objVal)


    # todo: extract information


if __name__ == '__main__':
    optimization_model()
