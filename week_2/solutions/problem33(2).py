# solution for 3.3
# author: Nick Szirbik
# date: 10 Feb 2022

import csv
# open and read the content of the comma separated values file


def read_and_print_content_of_file(file_name):
    with open(file_name) as handler_csv_file:
        raw_content_file = csv.reader(handler_csv_file)
    #       raw_content_file is a mere collection of characters

        table = list(raw_content_file)
    #       forcing (typecasting) the character collection into a list of lists

    print("unstructured file content = ", raw_content_file)
    print("file content as list of records = ", table)
    print("total number of data records =", len(table))

    print("table header = ", table[0])
    print("last record in the table = ", table[-1])

    print("name in the last record in the table = ", table[-1][0])
    print("data points in a record =", len(table[0]))


if __name__ == '__main__':
    read_and_print_content_of_file()
