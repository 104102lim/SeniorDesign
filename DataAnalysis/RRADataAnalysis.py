# -*- coding: utf-8 -*-
"""
  RRADataAnalysis.py
  Risk Reduction Activity for Data Analysis Module
  04/14/2018
"""

import pandas as pd
import numpy as np
import pyodbc
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


def connect():
    #*** Change parameters with your local SQL server.
    server = 'MSI\SQLEXPRESS'
    db = 'RiskReduction'
    
    cnxn = pyodbc.connect("DRIVER={SQL Server}; SERVER=" + server + "; DATABASE=" + db + "; Trusted_Connection=yes")
    cursor = cnxn.cursor()
    return cursor

def mergeFrames(frames, keys, framesToMerge):
    for mergeToIdx in range(1, len(framesToMerge)):
        mergeFromIdx = framesToMerge[0]
        #create new columns
        for col in frames[mergeFromIdx].columns.values:
            if col != keys[mergeFromIdx]:
                frames[mergeToIdx][col] = np.nan
                for idxTo in range(len(frames[mergeToIdx].index)):
                    for idxFrm in range(len(frames[mergeFromIdx].index)):
                        if frames[mergeToIdx].loc[idxTo][keys[mergeFromIdx]] == frames[mergeFromIdx].loc[idxFrm][keys[mergeFromIdx]]:
                            frames[mergeToIdx].set_value(idxTo, col, frames[mergeFromIdx].loc[idxFrm][col])
    del frames[mergeFromIdx]
    del keys[mergeFromIdx]

def getFrames(tableNames, cursor):
    frames = []
    for name in tableNames:
        cursor.execute('SELECT * FROM [dbo].[' + name + ']');
        table = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        dictArr = []
        for row in table:
            entry = {}
            for col in columns:
                entry[col] = row[columns.index(col)]
            dictArr.append(entry)
        frames.append(pd.DataFrame(dictArr))
    return frames
 
def idFramesToMerge(frames, keys):
    ret = []
    for idx in range(len(frames)): 
        commonKeys = []
        for col in list(frames[idx].columns.values):
            for key in keys:
                if key == col:
                    commonKeys.append(key)
        if len(commonKeys) == 1:
            frameWithOneKey = idx
            break
    ret.append(frameWithOneKey)

    for idx in range(len(frames)):
        for col in list(frames[idx].columns.values):
            if (col == commonKeys[0]) and (idx != ret[0]):
                ret.append(idx)
                break
    return ret
        


# (1) Database Preprocessing
cursor = connect()

tableNames = ['schools', 'classes', 'resources', 'students', 'teachers']
keys = ['SchoolID', 'ClassID', 'ResourceID', 'StudentID', 'TeacherID']

frames = getFrames(tableNames, cursor)

while len(keys) > 1:
    framesToMerge = idFramesToMerge(frames, keys)
    mergeFrames(frames, keys, framesToMerge)
    

#------------------------------------------------------------------------------
    
    
# (2) Data Analysis
dataset = frames[0]      # panda dataframe for merged dataset
COLUMN = dataset.columns # column list for "dataset"
NUM_COLUMN = COLUMN.size # number of columns in "COLUMN"

print "Single Merged Dataset: \n"
print dataset, '\n'


# do Linear Regression for each column
print "------------------ All Linear Regression ------------------"
threshold = 0 # threshold
count = 1     # number of total analysis

for i in range(0, NUM_COLUMN-1):
    for j in range(i+1, NUM_COLUMN):
        print str(count) + ". " + COLUMN[i] + " vs. " + COLUMN[j]
        count += 1
        
        # 0. set threshold
        threshold = 0
        
        # 1. get filtered two features
        mean_x = np.mean(dataset[COLUMN[i]])
        mean_y = np.mean(dataset[COLUMN[j]])
        # first feature
        for k in range(0, len(dataset[COLUMN[i]])):
            if dataset[COLUMN[i]][k] < threshold:
                dataset[COLUMN[i]][k] = mean_x
        # second feature
        for k in range(0, len(dataset[COLUMN[j]])):
            if dataset[COLUMN[j]][k] < threshold:
                dataset[COLUMN[j]][k] = mean_y
            
        # 2. do linear regression
        train_x = dataset[COLUMN[i]].reshape(-1, 1)
        train_y = dataset[COLUMN[j]]

        linearRegression = linear_model.LinearRegression()
        linearRegression.fit(train_x, train_y)

        pred_y = linearRegression.predict(train_x)

        # 3. plot the result
        title = COLUMN[i] + " vs. " + COLUMN[j]
        plt.title(title)
        plt.xlabel(COLUMN[i])
        plt.ylabel(COLUMN[j])
        plt.scatter(train_x, train_y,  color='blue')
        plt.plot(train_x, pred_y, color='orange', linewidth=3)
        plt.show()

        # 4. show indicators
        # Model coefficient(s)
        print '\nCoefficients:', linearRegression.coef_
        # Mean squared error
        print 'MSE:', mean_squared_error(train_y, pred_y)
        # Variance score: 1 is perfect prediction
        print 'R^2:', r2_score(train_y, pred_y)
        print '\n\n'


print "------------------ Selected Linear Regression ------------------"
firstFeature = str(input("Enter first feature: "))
secondFeature = str(input("Enter second feature: "))
threshold = int(input("Enter threshold: "))

print "\n" + firstFeature + " vs. " + secondFeature
       
# 1. get filtered two features
mean_x = np.mean(dataset[firstFeature])
mean_y = np.mean(dataset[secondFeature])
# first feature
for k in range(0, len(dataset[firstFeature])):
    if dataset[firstFeature][k] < threshold:
        dataset[firstFeature][k] = mean_x
# second feature
for k in range(0, len(dataset[secondFeature])):
    if dataset[secondFeature][k] < threshold:
        dataset[secondFeature][k] = mean_y
            
# 2. do linear regression
train_x = dataset[firstFeature].reshape(-1, 1)
train_y = dataset[secondFeature]

linearRegression = linear_model.LinearRegression()
linearRegression.fit(train_x, train_y)

pred_y = linearRegression.predict(train_x)

# 3. plot the result
title = firstFeature + " vs. " + secondFeature
plt.title(title)
plt.xlabel(firstFeature)
plt.ylabel(secondFeature)
plt.scatter(train_x, train_y,  color='blue')
plt.plot(train_x, pred_y, color='orange', linewidth=3)
plt.show()

# 4. show indicators
# Model coefficient(s)
print '\nCoefficients:', linearRegression.coef_
# Mean squared error
print 'MSE:', mean_squared_error(train_y, pred_y)
# Variance score: 1 is perfect prediction
print 'R^2:', r2_score(train_y, pred_y)
print '\n\n'


