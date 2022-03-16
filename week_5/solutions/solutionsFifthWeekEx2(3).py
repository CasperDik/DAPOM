# -*- coding: utf-8 -*-
"""
Created Sep 2020

@author: Nick Szirbik

purpose: didactic/ fifth DAPOM practical

"""
# file name: solutionsFifthWeekEx2
import sys, os

import pandas as pd
import numpy as np

def repairGender(gender):
    repairedGender = gender
    # if the string is not repaired after the code below, the same value
    # that was sent is returned
    if gender == 'f' or gender == 'female' or gender == 'F' or gender == 'fem.':
        repairedGender = 'Female'
    if gender == 'm' or gender == 'male' or gender == 'M' or gender == 'man':
        repairedGender = 'Male'

    return repairedGender

inputFile = 'phdThesesFrance1935_1990.csv'
df = pd.read_csv(os.path.join(sys.path[0], inputFile))

print(df.columns)

questionMarks = df[df['gender'] == '?'].index
df.drop(questionMarks, inplace = True)

df['gender'] = df['gender'].apply(repairGender)

outputFile = 'genderIsUniformNow.csv'
df.to_csv(os.path.join(sys.path[0], outputFile), index = False)

print("exit code 0")
