%reset -f

from gurobipy import Model, GRB, quicksum
import csv

# You may need to add the path of the file if Python gives the error it cannot
# find the file
with open("inv_control_data_2.txt") as handler_csv_file:
    raw_content_file = csv.reader(handler_csv_file)
    table = list(raw_content_file)

D=[0]
C=[0]

for record in table[1:]: #note the indexing, it skips the header
	D.append(int(record[0]))
	C.append(int(record[1]))

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
