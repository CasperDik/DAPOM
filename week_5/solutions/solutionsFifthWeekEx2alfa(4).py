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

def repairGender1(gender):
    repairedGender = gender
# using title
    gTitled = gender.title()
    if gTitled[0] == 'F':
        repairedGender = 'Female'
    if gTitled[0] == 'M':
        repairedGender = 'Male'

    return repairedGender

inputFile = 'phdThesesFrance1935_1990.csv'
df = pd.read_csv(os.path.join(sys.path[0],inputFile))

print(df.columns)

questionMarks = df[df['gender'] == '?'].index
df.drop(questionMarks, inplace = True)

df['gender'] = df['gender'].apply(repairGender1)

outputFile = 'genderIsUniformNow.csv'
df.to_csv(os.path.join(sys.path[0], outputFile), index = False)

print("exit code 0")
