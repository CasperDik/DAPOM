#!/usr/bin/python

# This example implements a scalable model for the product mix example
# of FP, Appendix 16.A. See eqs 16.107--16.113, but now with lists,
# for loops and functions

# Nicky van Foreest, 2019

from gurobipy import Model, GRB, quicksum

m = Model("product mix")

# profits
P = [45, 60]
# demands
D = [100, 50]

# machine capacities
C = [2400] * 4

# production times

PT = [[15, 10], [15, 35], [15, 5], [25, 14]]

num_products = len(P)
num_machines = len(C)

x = m.addVars(num_products, lb=0, ub=D, name="x")
# print(x) # just check to see what I get.

for i in range(num_machines):
    m.addConstr(quicksum(PT[i][j] * x[j] for j in range(num_products)) <= C[i])


m.setObjective(quicksum(P[i] * x[i] for i in range(num_products)), GRB.MAXIMIZE)

m.optimize()

for v in m.getVars():
    print("%s %g" % (v.varName, v.x))

print("Obj: %g" % m.objVal)
