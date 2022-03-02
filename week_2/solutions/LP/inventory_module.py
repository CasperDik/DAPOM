# a module for inventory control

from gurobipy import Model, GRB, quicksum


def optimize_inventory_with_param(D, C, r, h):
    m = Model("product mix")

    X = m.addVars(len(D), lb=0, name="production in period")
    S = m.addVars(len(D), lb=0, name="sales in period")
    I = m.addVars(len(D), lb=0, name="inventory at the end of period")

    for i in range(len(C)):
        m.addConstr(X[i]<=C[i])

    for i in range(len(D)):
        m.addConstr(S[i]<=D[i])

    m.addConstr(X[0]==0)
    m.addConstr(S[0]==0)
    m.addConstr(I[0]==0)

    for t in range(1, len(D)):
        m.addConstr(I[t]==I[t-1]+X[t]-S[t])

    m.setObjective(quicksum(r*S[t]-h*I[t] for t in range(1, len(D))), GRB.MAXIMIZE)

    m.optimize()

    for v in m.getVars():
        print("%s is: %g" % (v.varName, v.x))

    print("Objective attained for a profit of: %g" % m.objVal)
