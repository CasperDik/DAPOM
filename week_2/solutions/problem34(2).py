# solution 3.4
# author: Nick Szirbik
# date: 14 Feb. 2022

import csv


def make_table_from_file(file_name):
    # a function that reads the content of a file into a table
    with open(file_name) as handler_csv_file:
        raw_content_file = csv.reader(handler_csv_file)
        table = list(raw_content_file)
    return table


def inspect_record_legths(table):
    # a function that shows the length of all records
    for record in table:
        print(len(record))


def pretty_print_all(table):
    # pretty print the table
    for record in table[1:]: #note the indexing, it skips the header
        address = record[1]
        geolocation = record[2]
        name = record[0]
        print("\nAt:", address, "\ncoord.:", geolocation, "\nis:", name)


def catch_length_errors_automatically(table):
    expected_record_length = len(table[0])
    consistent = True
    for record in table[1:]:
        consistent = (len(record) == expected_record_length)
        if not consistent:
            print("ALERT, ALERT, ALERT")
            print(record, "has", len(record), "data points")
            break
        else:
            continue
    # the above one catches only the first one
    # if there are not problems, we should also indicate this to the user
    if consistent:
        print("KEEP cool: all records have the same value")
    # the code below catches all the bad lines
    expected_record_length = len(table[0])
    wrong_length_record_counter = 0
    for record in table[1:]:
        if not len(record) == expected_record_length:
            wrong_length_record_counter += 1
            print("ALERT", record, "has", len(record), "data points")
    print("In total", wrong_length_record_counter, "times, the record length is wrong")


def catch_errors_elegantly(table):
    # a more elegant alternative to the function above, which returns the corrected table
    incorrect_records = []
    expected_record_length = len(table[0])
    for record in table[1:]:
        if not(len(record) == expected_record_length):
            incorrect_records.append(record)

    print("In total", len(incorrect_records), "times, the record length is wrong")
    # we have now the bad records stored separately, and we can print them
    for bad_record in incorrect_records:
        print(bad_record, "bad length =", len(bad_record))

    # the above also helps to delete the incorrect length records from the table
    # we do it record by record iterating through the collected ones
    for bad_record in incorrect_records:
        table.remove(bad_record)
        print("one record removed from the table")
    return table