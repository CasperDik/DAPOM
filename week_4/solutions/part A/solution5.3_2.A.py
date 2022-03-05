# solution 5.3.2
# author: Nick Szirbik
# date: 23 Sept 2020
'''
reads a csv file in a data frame, creates a new score column
and sorts descending the rows based on the score, saving the data in a file
that has a new index, showing ranking (0-ascending)
'''

def nps_formula(g, b, u):
# computes the Net promoter score in a range from  0 to 10
    value = (g / (g + b + u) - b / (g + b + u)) * 5.0 + 5.0
    return value

import numpy as np
import pandas as pd
import os, sys

df = pd.read_csv(os.path.join(sys.path[0],'rankingsRaw.csv'),
                 sep = ',')
print(df.shape)
print(df.columns)
print(df.dtypes)
#print(df)

df['score'] = nps_formula(df.nrGoodReviews,
                          df.nrBadReviews,
                          df.nrUndecided)
# move the score upfront and keep the index
cols = list(df.columns)
df = df[[cols[-1]] + cols[0:2]]

# sort the table from the highest scoring restaurant down
df.sort_values(by = ['score'], ascending = False,
                ignore_index = True,
                inplace = True)
# when saving the file, the index column (first) will show also the ranking
df.to_csv(os.path.join(sys.path[0],'rankingsScores.csv'),
                 index= True, sep = ',')

#dfs.head()
#dfs.tail()
print("exit code 0")
