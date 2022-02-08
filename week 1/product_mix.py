from gurobipy import Model, GRB

m = Model("product mix")

x1 = m.addVar(vtype=GRB.CONTINUOUS, ub=100, name="x1")
x2 = m.addVar(vtype=GRB.CONTINUOUS, ub=50, name="x2")

m.setObjective(45 * x1 + 60 * x2, GRB.MAXIMIZE)

m.addConstr(15 * x1 + 10 * x2 <= 2400)
m.addConstr(15 * x1 + 35 * x2 <= 2400)
m.addConstr(15 * x1 + 5 * x2 <= 2400)
m.addConstr(25 * x1 + 14 * x2 <= 2400)

m.optimize()

for v in m.getVars():
    print("%s %g" % (v.varName, v.x))

print("Obj: %g" % m.objVal)
