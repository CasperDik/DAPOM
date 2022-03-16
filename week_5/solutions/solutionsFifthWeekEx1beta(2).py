# -*- coding: utf-8 -*-
"""
Created Sep 2020

@author: Nick Szirbik

purpose: didactic/ fifth DAPOM practical

"""
# file name: solutionsFifthWeekEx1beta
import sys, os

import pandas as pd
import numpy as np

inputFile = 'phdThesesFrance1935_1990.csv'
# inputFile = 'genderIsUniformNow.csv'
df = pd.read_csv(os.path.join(sys.path[0], inputFile))

print('ways the gender field appears:',
      df['gender'].nunique(), 'kinds\n',
      'each occurs:\n kind   occurences\n',
      df['gender'].value_counts())

waysBD = df['year_of_birth'].nunique()
print(df['year_of_birth'].value_counts())
print('ways to see the year field:', waysBD)

pd.set_option('display.max_rows', waysBD)
print(df['year_of_birth'].value_counts())

print('exit code 0')
