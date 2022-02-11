# Homework from chapter 2 DAPOM Python manual
# Author: Nick Szirbik
# date: 6 Feb. 2022

from inspect_file import show_file_content
from quadratic_equation import solve_quadratic_with_the_following_parameters_and_print_solutions, \
                            solve_quadratic_with_user_input_and_return_solutions


def execute():
    # first exercise, note the passing of the name of the file as parameter
    show_file_content("storage.txt")
    # second exercise, solving a quadratic equation
    # first, send the actual values of the parameters
    solve_quadratic_with_the_following_parameters_and_print_solutions(c=1, b=2, a=-2)
    # notice that we can alter the order of the parameters, but ONLY if we specify explicitly their names
    # second, let the user input them, and have the two values returned
    solutions = solve_quadratic_with_user_input_and_return_solutions()
    print("x1 = %g and x2 = %g" %(solutions))


if __name__ == '__main__':
    execute()
