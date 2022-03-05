# solution 5.3.1
# author: Nick Szirbik
# date: 23 Sept 2020
'''
reads a csv file in a data frame, inspects its content and structure,
and adds three empty columns via a Data Frame operations,
and saves the new data structure into a new csv file,
changing also the separators from semicolon to semicolon
'''

import numpy as np
import pandas as pd
import os, sys

df = pd.read_csv(os.path.join(sys.path[0],'restRanking.csv'), sep = ';')
print(df.shape)
print(df.columns)
print(df.dtypes)
#print(df)

# adding zero populated columns in a very bad way...
# zeroes = [0] * df.shape[0]
# df['nrGoodReviews'] = zeroes
# df['nrBadReviews'] = zeroes
# df['nrUndecided'] = zeroes

# add three "empty columns"
for newCol in ['nrGoodReviews','nrBadReviews', 'nrUndecided']:
    df[newCol] = None

# sort the data frame alphabetically
dfs = df.sort_values(by = ["name", "address"])
dfs.to_csv(os.path.join(sys.path[0],'restRankingEmpty.csv'),
          index = False, sep = ',')
# below, good programming practice, to finish any script/code that is
# executed in batch mode - this is done also in C, C++, Java and other...
print("exit code 0")
# this print, if executed, signals to us that the program ended normally
# and this is useful when your script does not output anything else
