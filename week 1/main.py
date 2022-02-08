"""
purpose: optimize the cost of a healthy bimimbap preparation
author: Nick Szirbik
date: 7 of Feb. 2022
"""
from gurobipy import Model, GRB
import cp  # constant parameters assigned to a, b, c named variables in a separate file, cp.py

m = Model("diet optimization")

# each variable denotes quantity, in 100g units (e.g. x1 = 0.5, means 50g of pearl barley)
x1 = m.addVar(ub=0.7, name="pearl barley")
x2 = m.addVar(name="tofu")
x3 = m.addVar(ub=0.4, name="kimchi")
x4 = m.addVar(ub=0.6, name="mushroom")
x5 = m.addVar(ub=0.5, name="onion")
x6 = m.addVar(name="oil")

# setting constraint on minimum protein per portion
m.addConstr(cp.a11 * x1 + cp.a12 * x2 + cp.a13 * x3 + cp.a14 * x4 + cp.a15 * x5 + cp.a16 * x6 >= cp.b1)
# setting constraint on minimum carbs per portion
m.addConstr(cp.a21 * x1 + cp.a22 * x2 + cp.a23 * x3 + cp.a24 * x4 + cp.a25 * x5 + cp.a26 * x6 >= cp.b2)
# setting constraint on minimum fat per portion
m.addConstr(cp.a31 * x1 + cp.a32 * x2 + cp.a33 * x3 + cp.a34 * x4 + cp.a35 * x5 + cp.a36 * x6 >= cp.b3)
# setting constraint on minimum fibre per portion
m.addConstr(cp.a41 * x1 + cp.a42 * x2 + cp.a43 * x3 + cp.a44 * x4 + cp.a45 * x5 + cp.a46 * x6 >= cp.b4)

# setting an objective function that yields the price of a portion
m.setObjective(cp.c1 * x1 + cp.c2 * x2 + cp.c3 * x3 + cp.c4 * x4 + cp.c5 * x5 + cp.c6 * x6, GRB.MINIMIZE)

m.optimize()

for v in m.getVars():
    print("%s %g" % (v.varName, v.x))
# prices are per kilogram, therefore scaling down by 10 is necessary to see price per portion
print("Objective attained at: %g" % (m.objVal))
