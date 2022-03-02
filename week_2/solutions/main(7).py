# This is the testing script used for the homework for week 2
# author: Nick Szirbik
# date: 10th of February 2022

from problem33 import read_and_print_content_of_file
from problem34 import make_table_from_file, \
                    inspect_record_legths, pretty_print_all, \
                    catch_length_errors_automatically, \
                    catch_errors_elegantly
from problems35 import checking_various_criteria
from problem36 import add_multiple_restaurants_to, add_a_restaurant_to_table, \
                    create_new_file
# you can run the items for homework selectively, by commenting out parts you do not want to clutter your output
# pane. However, if you use any function that gets "restaurants" or a table as parameter, you have first to create
# that table, and the obvious function that does this is make_table_from_file(). If you do not this first, you will
# not have the data in the memory.


def run_week3_homework_items():
    # read_and_print_content_of_file("groningenRestaurants.csv")
    restaurants = make_table_from_file("groningenRestaurants.csv")
    # inspect_record_legths(restaurants)
    pretty_print_all(restaurants)
    # catch_length_errors_automatically(restaurants)
    # repaired_restaurants = catch_errors_elegantly(restaurants)
    # pretty_print_all(repaired_restaurants)
    # checking_various_criteria(restaurants)
    # restaurants_plus_one = add_a_restaurant_to_table(restaurants)
    # create_new_file(restaurants_plus_one, "gRplusOne.csv")
    restaurants_with_more_added = add_multiple_restaurants_to(restaurants)
    create_new_file(restaurants_with_more_added, "gRplusMany.csv")


if __name__ == '__main__':
    run_week3_homework_items()
