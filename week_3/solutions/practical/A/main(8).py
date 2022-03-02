# This is a Python script that runs various parts of the exercises and code
# from chapter 4 of the Python manual.
# author: Nick Szirbik, 16 Feb. 2022

import pandas as pd
from statistics import mean
from module_for_4_3_and_4_4 import create_F1_dictionary, \
    explore_dataframe, save_data_frame_to_csv_file, \
    add_teams_column, delete_gender_column, \
    print_only_a_team_wins, print_only_a_team_and_a_champ_wins


def exercise_4_3a():
    formula_One_fifties = create_F1_dictionary()
    # adding the gender information
    formula_One_fifties["gender"] = ["m"] * 10
    # print it ugly...
    print("raw dictionary dump: \n", formula_One_fifties)

    # ... and print it nicely, by making it first a Panda DataFrame object
    formula_One_frame = pd.DataFrame(formula_One_fifties, columns=[
        "year", "champ", "wins", "points", "gender"
    ])
    print("printing as a pandas DataFrame object:")
    print(formula_One_frame)
    return formula_One_frame


if __name__ == '__main__':
    # create the frame first
    f1_frame = exercise_4_3a()
    # do the rest of 4.3
    # look at some characteristics of the dataframe
    explore_dataframe(f1_frame)
    save_data_frame_to_csv_file(f1_frame, "f1_fifties.csv")
    # open the "f1_fifties.csv" file and have a look...
    f1_frame = add_teams_column(f1_frame)
    # added Team names
    print(f1_frame)
    # deleting the gender column
    f1_frame = delete_gender_column(f1_frame)
    print(f1_frame)

    #do the actions specified in 4.4
    # print the first five and the last three
    print(f1_frame.head())
    print(f1_frame.tail(3))

    # print the last four
    print(f1_frame["champ"][-4:])

    # print only Ascari
    print(f1_frame[["champ", "year"]][2:4])

    # make statistics
    print("average point score in the fifties:", mean(f1_frame["points"]))

    # 4.4
    print_only_a_team_wins(f1_frame, "Maserati")
    print_only_a_team_and_a_champ_wins(f1_frame, team="Ferrari", champ="Fangio")

    # 4.5
    # because this file is becoming too big, maybe a better idea is to make a separate
    # project for this subchapter. The exercises are in a single function in module_4_5.py
    # this big function could be broken into smaller function
    # you can run the function in the module_4_5 by importing the name here,
    # or run it directly from the module, thanks to the if __name__ == "__main__" construct
