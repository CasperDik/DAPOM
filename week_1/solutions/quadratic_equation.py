# solution 2.5
# part of the solution set for DAPOM practical week 1
# author: Nick Szirbik
# date: 6 Feb 2022

# Solve the quadratic equation ax**2 + bx + c = 0 with values set in the
# program

def solve_quadratic_with_the_following_parameters_and_print_solutions(a: float = 0, b: float = 0, c: float = 0):
    # calculate the discriminant
    d = (b ** 2) - (4 * a * c)

    # find two solutions
    sol1 = (-b - d ** 0.5) / (2 * a)
    sol2 = (-b + d ** 0.5) / (2 * a)

    print('The solutions are ', sol1, sol2)


def solve_quadratic_with_user_input_and_return_solutions():
    # Solve the quadratic equation ax**2 + bx + c = 0 with values taken from
    # keyboard, given by the program's user

    # To take coefficient input from the users
    a = float(input('Enter a: '))
    b = float(input('Enter b: '))
    c = float(input('Enter c: '))

    # calculate the discriminant
    d = (b ** 2) - (4 * a * c)

    # find two solutions
    sol1 = (-b - d ** 0.5) / (2 * a)
    sol2 = (-b + d ** 0.5) / (2 * a)

    return sol1, sol2
