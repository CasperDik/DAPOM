
# solution 5.3.1
# author: Nick Szirbik
# date: 23 Sept 2020
'''
creating restRanking.csv file from groningenRestaurants
'''

import sys, os
import pandas as pd
import numpy as np
from random import randint, seed

df = pd.read_csv(os.path.join(sys.path[0],"groningenRestaurants.csv"))

# get rid of the geolocation data
df1 = df.drop("lonlat", axis = 1)
# rename the columns
df1.columns = ["name", "address"]

df1.to_csv(os.path.join(sys.path[0],'restRanking.csv'), index = False, sep = ';')

# add randomly generated "survey" data
df1['nrGoodReviews'] = [randint(df.shape[0] - i + 99, 777) for i in range(df1.shape[0])]
df1['nrBadReviews'] = [randint(i, 555) for i in range(df1.shape[0])]
df1['nrUndecided'] = [randint(1, 666) for i in range(df1.shape[0])]

df1.to_csv(os.path.join(sys.path[0],'rankingsRaw.csv'), index = False, sep = ',')

print("exit 0")
