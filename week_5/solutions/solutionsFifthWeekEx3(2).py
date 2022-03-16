# -*- coding: utf-8 -*-
"""
Created Sep 2020

@author: Nick Szirbik

purpose: didactic/ fifth DAPOM practical

"""
# file name: solutionsFifthWeekEx3
import os, sys

import pandas as pd
import numpy as np

def repairYearOfBirth(year):
    repairedYear = year
    # if no changes are made, the initial value is returned
    repairedYear = repairedYear.replace('c.', '')
    # if the date starts with the 'c.', this is eliminated
    # otherwise it remains the same
    repairedYear = repairedYear.replace('C.', '')
    # if the date starts with the 'C.', this is eliminated
    # otherwise it remains the same
    repairedYear = repairedYear.replace('(', '')
    repairedYear = repairedYear.replace(')', '')
    # if the parantheses are present they are eliminated
    # if the dash is in the year string
    if '-' in repairedYear:
        years = repairedYear.split('-')
        # then a list of two year strings is created
        # and the average year is computed in between
        repairedYear = str(int(round(int(years[0]) + int(years[1]))/2))
        # to be consistent, the repaired year is typecast into string
        # from an integer average that is typecast from a float
        # NOTE: the result of the round() function is a float!

    return repairedYear

inputFile = 'genderIsUniformNow.csv'
df = pd.read_csv(os.path.join(sys.path[0], inputFile))

print(df.columns)

df['year_of_birth'] = df['year_of_birth'].apply(repairYearOfBirth)

outputFile = 'genderAndYearAreUniformNow.csv'
df.to_csv(os.path.join(sys.path[0], outputFile), index = False)

print("exit code 0")
