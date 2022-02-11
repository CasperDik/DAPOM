# This is a Python script to experiment with an optimization model
# Author: Nick Szirbik
# date: 10 Feb. 2022

from week_1.solutions.LP.gurobi_model_product_mix import optimize_product_mix
from week_1.solutions.LP.gurobi_model_product_mix_fifth_machine import product_mix_with_fifth_machine
from week_1.solutions.LP.gurobi_model_product_mix_third_product import optimize_product_mix_with_three_products
from week_1.solutions.LP.gurobi_model_product_mix_minimal_capacity import optimize_product_mix_for_capacity_minimization


def execute(name):
    print(f'APPLICATION {name}')
    optimize_product_mix()
    product_mix_with_fifth_machine()
    optimize_product_mix_with_three_products()
    optimize_product_mix_for_capacity_minimization()


if __name__ == '__main__':
    execute('OPTIMIZATION STARTED')

