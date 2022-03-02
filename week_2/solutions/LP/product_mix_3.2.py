#!/usr/bin/python

# This example implements a scalable model for the product mix example
# of FP, Appendix 16.A. See eqs 16.107--16.113, but now with lists,
# for loops and functions

# Nicky van Foreest, 2019


from gurobipy import Model, GRB, quicksum

P = [45, 60]  # profits
D = [100, 50]  # demands
C = [2400] * 4  # machine capacities

# production times
PT = [[15, 10], [15, 35], [15, 5], [25, 14]]


def optimize(P, D, C, PT):
    """
    P: list with product profits
    D: list with product demands
    C: list with machine capacities
    PT: list of lists: production time of product per machine

    """
    m = Model("product mix")

    num_products = len(P)
    num_machines = len(C)

    x = m.addVars(num_products, lb=0, ub=D, name="x")

    for i in range(num_machines):
        m.addConstr(quicksum(PT[i][j] * x[j] for j in range(num_products)) <= C[i])

    m.setObjective(quicksum(P[i] * x[i] for i in range(num_products)), GRB.MAXIMIZE)

    m.optimize()

    return m.objVal


res = optimize(P, D, C, PT)
print(res)
