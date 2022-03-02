# This example implements a scalable model for the product mix example
# of FP, Appendix 16.A. See eqs 16.107--16.113, but now with lists,
# for loops and functions

# Nicky van Foreest, 2019
# slightly changed, Nick Szirbik, 2022

from gurobipy import Model, GRB, quicksum


def optimze_product_mix_ex3_1(P, D, C, PT):
    """
        P: list with product profits
        D: list with product demands
        C: list with machine capacities
        PT: list of lists: production time of product per machine
        """
    m = Model("product mix")

    num_products = len(P)
    num_machines = len(C)

    x = m.addVars(num_products, lb=0, ub=D, vtype=GRB.INTEGER, name="production volume per week product")
    # print("just see how gurobi variables look like:", x) # just check to see what I get.

    for i in range(num_machines):
        m.addConstr(quicksum(PT[i][j] * x[j] for j in range(num_products)) <= C[i])

    m.setObjective(quicksum(P[i] * x[i] for i in range(num_products)), GRB.MAXIMIZE)

    m.optimize()

    for v in m.getVars():
        print("%s is: %g" % (v.varName, v.x))

    print("Objective attained with profit: %g" % m.objVal)
