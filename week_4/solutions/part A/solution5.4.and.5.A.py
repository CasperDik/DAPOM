# solution 5.4
# author: Nick Szirbik
# date: 23 Sept 2020
'''
various statistis and graphical output
'''

import numpy as np
import pandas as pd
import os, sys

df = pd.read_csv(os.path.join(sys.path[0],'rankingsScores.csv'), sep = ',')
print(df.shape)
print(df.columns)
print(df.dtypes)
# better delete the first column (the index is replicated in Unnamed:0 )
df.pop(df.columns[0])
# delete some scores in the input file (leave commas untouched)
# or add new lines with the score empty
print(df['score'].count())
print(df.count())

print(df['score'].min())
print(df['score'].max())
print(df.min())
print(df.max())

print(df['score'].mean())
print(df.mean())

print(df['score'].std())
print(df['score'].sum()) 		# Total sum of the column values
print(df['score'].median())		# Median of the column values
print(df['score'].nunique())	# Number of unique entries

print(df.describe()) 	# here the default is [0.25, 0.5, 0.75], which
# returns the 25th, 50th, and 75th percentiles
print(df.describe(percentiles = [0.15, 0.3, 0.45, 0.6, 0.85 ]))

# make a histogram
df['score'].hist()
df.hist()

# just to make a pie
df = pd.DataFrame({'mass' : [0.330, 4.87 , 5.972],
                   'radius' : [2439.7, 6051.8, 6378.1]},
                    index = ['Mercury', 'Venus', 'Earth'])
# we can select only one key/row if we want
df.plot.pie(y='mass', figsize=(5, 5))
df.plot.pie(y='radius', figsize=(5, 5))
# but we can also plot all in one shot
df.plot.pie(subplots = True, figsize = (6,3))

print("exit code 0")
