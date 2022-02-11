"""

With this example we compute the minimally required capacity to
satisfy all demand for the product mix example of FP, Appendix 16.A.
See eqs 16.107--16.113.


Petra de Jonge, Nicky van Foreest, 2019
updated Nick Szirbik 2022
"""

from gurobipy import Model, GRB


def optimize_product_mix_for_capacity_minimization():
    m = Model("product mix")

    # variables for products, as before
    x1 = m.addVar(name="product 1 units made per week")
    x2 = m.addVar(name="product 2 units made per week")
    # variables for capacity, replacing the previously fixed one at 2400 minutes
    c1 = m.addVar(name="minimum capacity per week machine A")
    c2 = m.addVar(name="minimum capacity per week machine B")
    c3 = m.addVar(name="minimum capacity per week machine C")
    c4 = m.addVar(name="minimum capacity per week machine D")

    # the objective is only about capacity, the production levels are only limited to max. sales
    m.setObjective(c1 + c2 + c3 + c4, GRB.MINIMIZE)

    m.addConstr(15 * x1 + 10 * x2 <= c1)
    m.addConstr(15 * x1 + 35 * x2 <= c2)
    m.addConstr(15 * x1 + 5 * x2 <= c3)
    m.addConstr(25 * x1 + 14 * x2 <= c4)

    m.addConstr(x1 >= 100)
    m.addConstr(x2 >= 50)

    # Of course we could have absorbed the constraints on x1 and x2 in the
    # methods addVar above, using ub=. Here we implemented it as explicit
    # constraints to make the shift in interpretation of the problem explicit.

    m.optimize()

    for v in m.getVars():
        print("%s is: %g" % (v.varName, v.x))

    print("Objective total minimum capacity is: %g" % m.objVal)
