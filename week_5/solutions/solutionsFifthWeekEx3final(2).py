# -*- coding: utf-8 -*-
"""
Created Sep 2020

@author: Nick Szirbik

purpose: didactic/ fifth DAPOM practical

"""
# file name: solutionsFifthWeekEx3final
import sys, os

import pandas as pd
import numpy as np

# now the input file is not only neat, but also contains clean
# i.e. uniformoulsy formatted data points
inputFile = 'genderAndYearAreUniformNow.csv'
df = pd.read_csv(os.path.join(sys.path[0], inputFile))

# create first integer columns instead of string columns
df['birthYear'] = df['year_of_birth'].apply(lambda year: int(year))
df['defYear'] = df['year_of_defense'].apply(lambda year: int(year))
# compute the age of the PhD at the time of thesis defense
df['defAge'] = df['defYear'] - df['birthYear']

print('average age to defend:', df['defAge'].mean())

# create two separate data frames for female and males
dfF = df[df['gender'] == 'Female']
dfM = df[df['gender'] == 'Male']

# answer the initial questions for the analysis
print('average female age to defend:', dfF['defAge'].mean())
print('average male age to defend:', dfM['defAge'].mean())

print("exit code 0")
