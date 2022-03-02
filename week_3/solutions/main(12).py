# This is a Python script to test various data frame features.
import datetime
from module_my_pandas_functions import read_big_file, do_stats_for, \
    iterate_through_entire, save_only_Sub_Saharan_Africa

file_name = '5m Sales Records.csv'

if __name__ == "__main__":
    table = read_big_file(file_name)
    do_stats_for(table)
    starting_moment = datetime.datetime.now()
    iterate_through_entire(table)
    print("iterating through 5M row took:", datetime.datetime.now() - starting_moment)
    save_only_Sub_Saharan_Africa(table)

