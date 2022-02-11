#!/usr/bin/python

# This example  implements the product mix example of FP,
# Appendix 16.A. See eqs 16.107--16.113.

# Nicky van Foreest, 2019
# update Nick Szirbik, Feb. 2022

from gurobipy import Model, GRB


def optimize_product_mix_with_three_products():
    m = Model("product mix")

    # the variables represent quantities of products manufactured in one week
    x1 = m.addVar(ub=100, name="product one") # the upper bound is due to the max. sales possible
    x2 = m.addVar(ub=50, name="product two")  # for product two only 50 units can be sold in a week
    x3 = m.addVar(lb=0, ub=20, name="product three")

    # the value of the objective function yields profit (in $)
    # selling a unit of product one yields $45
    # selling a unit of product two yields $65
    # the costs for producing product three are 30, and the price is 120
    m.setObjective(45 * x1 + 60 * x2 + (120 - 30) * x3, GRB.MAXIMIZE)

    m.addConstr(15 * x1 + 10 * x2 <= 2400) # this constraint is for machine A
    m.addConstr(15 * x1 + 35 * x2 <= 2400) # this constraint is for machine B
    m.addConstr(15 * x1 + 5 * x2 <= 2400)  # this constraint is for machine C
    m.addConstr(25 * x1 + 14 * x2 <= 2400) # this constraint is for machine D
    # fixed parameters are representing minutes (capacity of a machine)
    # 2400 min = 5 days * 8 hours shift time

    m.optimize()

    for v in m.getVars():
        print("quantity for %s is %g" % (v.varName, v.x))

    print("Objective profit attained with a third product: %g dollars$" % m.objVal)