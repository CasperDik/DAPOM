def inventory_control(D, C, I0, h, r):
    from gurobipy import Model, GRB, quicksum

    # time is length of the demand array
    t = len(D)

    # initiate model
    m = Model("Inventory control")

    # add decision variables
    X = m.addVars(t, lb=0.0, ub=C, vtype=GRB.CONTINUOUS, name="X")
    I = m.addVars(t, lb=0.0, vtype=GRB.CONTINUOUS, name="I")
    S = m.addVars(t, lb=0.0, ub=D, vtype=GRB.CONTINUOUS, name="S")

    # add constraints
    m.addConstr(X[0] == 0)
    m.addConstr(S[0] == 0)
    m.addConstr(I[0] == I0)
    m.addConstrs(I[i-1] + X[i] - S[i] == I[i] for i in range(1, t))

    # set objetive and optimize
    m.setObjective(quicksum(r*S[i] - h*I[i] for i in range(t)), GRB.MAXIMIZE)
    m.optimize()

    # print results
    for v in m.getVars():
        print("%s  %g" % (v.varName, v.x))

    print("Obj: %g" % m.objVal)

    inv = [v.X for k, v in I.items()]

    return inv

def import_C_and_D(filename):
    import numpy as np

    # import data from txt
    data = np.loadtxt(filename, delimiter=",", dtype=int)
    # from nested list to two seperate lists
    D, C = map(list, zip(*data))
    # insert 0 at t=0
    D = np.insert(D, 0, 0, axis=0)
    C = np.insert(C, 0, 0, axis=0)

    return D, C

def plot_inventory(inv):
    import matplotlib.pyplot as plt

    t = range(len(inv))
    plt.plot(t, inv)
    plt.show()


if __name__ == "__main__":
    # define demand and capacity
    D, C = import_C_and_D("inv_control_data_2.txt")

    # define some constants
    I0 = 0
    h = 1
    r = 10

    inv = inventory_control(D, C, I0, h, r)
    plot_inventory(inv)
