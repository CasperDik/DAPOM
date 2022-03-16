# -*- coding: utf-8 -*-
"""
Created Sep 2020

@author: Nick Szirbik

purpose: didactic/ fifth DAPOM practical

"""
# file name: solutionsFifthWeekEx1alfa
import os, sys

import pandas as pd
import numpy as np

inputFile = 'phdThesesFranceThirteesToNineties.csv'

df = pd.read_csv(os.path.join(sys.path[0], inputFile), encoding = 'latin-1')

print(df.shape)
print(df.columns)
print(df.dtypes)
print(df)

print('year range:',
      df['year_of_defense'].min(),
      '-',
      df['year_of_defense'].max())

odf = df.sort_values(by = ['gender'])

print('ways the gender field appears:',
      df['gender'].nunique(), 'kinds\n',
      'each occurs:\n kind   occurences\n',
      df['gender'].value_counts())

waysBD = df['year_of_birth'].nunique()
print(df['year_of_birth'].value_counts())
print('ways to see the year field:', waysBD)

pd.set_option('display.max_rows', waysBD)
print(df['year_of_birth'].value_counts())

outputFile = 'phdThesesFrance1935_1990.csv'
df.to_csv(os.path.join(sys.path[0], outputFile), index = False)

print('normal.termination.solutionsFifthWeekEx1alfa')
