# solution 4.3 and 4.4 from Python manual
# author: Nick Szirbik
# date: 17 Feb 2022

import pandas as pd
# define a dictionary directly in the code
# basically, this is a table, but dictionaries are versatile
# and can be used for other kinds of less structured datapoints


def create_F1_dictionary():
    data_in_dict = { "year" : [
                1950, 1951, 1952,
                1953, 1954, 1955,
                1956, 1957, 1958, 1959
                ],
             "champ" : [
                "Farina", "Fangio", "Ascari", "Ascari",
                "Fangio", "Fangio", "Fangio", "Fangio",
                "Hawthorne", "Brabham"
                ],
             "wins" : [
                3, 3, 6, 5,
                6, 4, 3, 4, 1, 2
                ],
             "points" : [
                30, 31, 36, 34,
                42, 40, 30, 40, 42, 43
                ]
            }
    return data_in_dict


def explore_dataframe(df:pd.DataFrame):
    # print the meta-information about the DataFrame sent as argument
    print("the size of the table is (rows * columns):")
    print(df.shape)
    print("the rows are organized as:")
    print(df.columns)
    print("the Python type of the values on the columns are:")
    print(df.dtypes)


def save_data_frame_to_csv_file(df: pd.DataFrame, file_name: str =""):
    # save the information in the DataFrame object to a .csv File
    # this time, with a specialized method from the Pandas library
    df.to_csv(file_name)
    print('data frame written to csv file f1_fifties.csv')


def add_teams_column(df):
    team_wins = ["Alfa Romeo"] * 2 + ["Ferrari"] * 2 + ["Mercedes"
        ] * 2 + ["Ferrari", "Maserati", "Ferrari", "Cooper"]

    df["team"] = team_wins
    return df


def delete_gender_column(df):
    # boy only club :-(
    del(df["gender"])
    return df


def print_only_a_team_wins(df, team_name: str = ""):
    # make a smaller DataFrame object, selecting from the big one
    only_a_team_seasons = df[df['team'] == team_name]
    print(type(only_a_team_seasons))
    print(only_a_team_seasons)


def print_only_a_team_and_a_champ_wins(df, champ, team):
    # selecting on two conditions
    only_a_champ_seasons = df[df['champ'] == champ]
    only_a_champ_driving_for_a_specific_team_seasons = only_a_champ_seasons[
        only_a_champ_seasons['team'] == team]
    print(only_a_champ_driving_for_a_specific_team_seasons)
