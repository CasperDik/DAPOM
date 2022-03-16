# -*- coding: utf-8 -*-
"""
Created Sep 2020

@author: Nick Szirbik

purpose: didactic/ fifth DAPOM practical

"""
# file name: solutionsFifthWeekEx1

import sys, os
import pandas as pd


df = pd.read_csv(os.path.join(sys.path[0], 'phdThesesFranceThirteesToNineties.csv'),
                encoding = 'latin-1')

print(df.shape)
print(df.columns)
print(df.dtypes)
print(df)

print('year range:',
      df['year_of_defense'].min(),
      '-',
      df['year_of_defense'].max())

odf = df.sort_values(by = ['gender'])

print('ways the gender field appears:', df['gender'].nunique(),
      '\neach occurs:\n',
      df['gender'].value_counts()
      )

outputFile = 'phdThesesFrance1935_1990.csv'
odf.to_csv(os.path.join(sys.path[0], outputFile), index = False)

print('exit code 0')
