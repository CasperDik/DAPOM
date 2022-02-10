from gurobipy import Model, GRB
import numpy as np

m = Model("product mix")

d = [100, 50]
pt = [[15, 10], [15, 35], [15, 5], [25, 14]]
c = [2400, 2400, 2400, 2400]
p = [45, 60]

x = m.addVars(2, ub=d, vtype=GRB.CONTINUOUS)
m.setObjective(p[0] * x[0] + p[1] * x[1], GRB.MAXIMIZE)

for i in range(len(c)):
    m.addConstr(pt[i][0] * x[0] + pt[i][1] * x[1] <=c[i])

m.optimize()

for v in m.getVars():
    print("%s %g" % (v.varName, v.x))

print("Obj: %g" % m.objVal)


