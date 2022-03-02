# solution 3.6 with function definition
# author: Nick Szirbik
# date: 14 Feb 2022

import csv


def readRestaurantData(header):
  record =[]
  for datapoint in header:
      value = input(datapoint + "= ")
      record.append(value)
  return record
# OBSERVE: this function works for any input file with any table header
# it has the main quality of a function - it can be reused again and again
# without changing it


def add_a_restaurant_to_table(table):
    name = input("restaurant name is: ")
    address = input("restaurant address is: ")
    lonlat = input("coordinates are: ")
    new_row = list((name, address, lonlat))
    table.append(new_row)
    print(table[-1], "added!")
    return table


def create_new_file(table, file_name):
    with open(file_name, mode="w", newline='') as handler:
        file_writer = csv.writer(handler, quotechar = '"', quoting=csv.QUOTE_ALL)
                        # necessary to put quotes when commas appear in a data point
                        # and have the same format with the rest of the existing file
        for row in table:
            file_writer.writerow(row)
    print("new file:", file_name, "created")


def add_multiple_restaurants_to(table):
    # use a while statement to repeat a statement block until y is inputted by the user
    stop = False
    while not stop:
        new_Restaurant = readRestaurantData(table[0])
    # the function gets the table header as argument and returns one full data records
    # for one restaurant - if the header is longer than 3, it will work anyway
        if (input("stop? y/n") == 'y'):
            stop = True
        table.append(new_Restaurant)
    return table

