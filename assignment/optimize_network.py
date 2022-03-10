from gurobipy import Model, GRB, quicksum
from itertools import product
import numpy as np


def demand():
    # demand drops with 5% for 1 min cycling
    # todo: check lecture recordings
    demand_pickup = 0.35 - 0.05 / 60 * travel_time_on_bike_in_seconds
    return W
m = Model("Locker optimization")

# todo: import D, W

n = 10 # todo: len(D) is W symmetric then true otherwise check both len of i and j
W = np.random.rand(n, n) # W = demand()
D = np.random.rand(n)
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
