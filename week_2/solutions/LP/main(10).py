# This is Python script containing code for DAPOM exercises from the LP manual chapter 3.
# author: Nick Szirbik

from optimizer_product_mix_3_1 import optimze_product_mix_ex3_1
from optimizer_product_mix_3_2 import optimze_product_mix_ex3_2
from inventory_module import optimize_inventory_with_param
from inventory_from_file import optimize_inventory_using_data_from_file

profits_per_product = [45, 60]  # profits
demands_per_product = [100, 50]  # demands
capacities_per_machine = [2400] * 4  # machine capacities
production_times_per_machine_per_product = [[15, 10], [15, 35], [15, 5], [25, 14]]  # production times


def do_exercise_1():
    # exercise 1
    # invoke a function that only prints the results of the optimization
    optimze_product_mix_ex3_1(profits_per_product,
                              demands_per_product,
                              capacities_per_machine,
                              production_times_per_machine_per_product)


def do_exercise_2():
    # exercise 2
    # invoke a function that RETURN the results of the optimization
    variables, objective = optimze_product_mix_ex3_2(profits_per_product,
                                                     demands_per_product,
                                                     capacities_per_machine,
                                                     production_times_per_machine_per_product)
    for v in variables:
        print("%s is: %g" % (v[0], v[1]))

    print("Objective attained with profit: %g" % objective)


def do_exercise_3_and_4():
    # exercise 3
    # plan production and inventory exercise
    D = [0, 80, 100, 120, 140, 90, 140]  # demand per period
    C = [0, 100, 100, 100, 120, 120, 120]  # capacity per period
    # r is profit per unit, h is holding cost per unit per period
    optimize_inventory_with_param(D, C, r=10, h=1)

    # exercise 4
    optimize_inventory_using_data_from_file("inv_control_data_2.txt", r=10, h=1)
    # uncomment and comment selectively parts of the above code to run only one exercise at a time


if __name__ == '__main__':
    do_exercise_1()
    do_exercise_2()
    do_exercise_3_and_4()
