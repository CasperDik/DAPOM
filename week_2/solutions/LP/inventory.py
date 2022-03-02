%reset -f

from gurobipy import Model, GRB, quicksum

D = [0, 80, 100, 120, 140, 90, 140]
C = [0, 100, 100, 100, 120, 120, 120]

r = 10
h = 1

m = Model("product mix")

X = m.addVars(len(D), lb=0, name="x")
S = m.addVars(len(D), lb=0, name="s")
I = m.addVars(len(D), lb=0, name="i")

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
    print("%s %g" % (v.varName, v.x))

print("Obj: %g" % m.objVal)
