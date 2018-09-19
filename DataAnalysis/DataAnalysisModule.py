# -*- coding: utf-8 -*-
"""
    -----------------------------------------------------------------------
    DataAnalysisModule.py
    : Data Analysis Module for Software Applcation
    Author: Sungho Lim, Joey Gallardo
    09/16/2018
    -----------------------------------------------------------------------
    """


#-----------------------------------------------------------------------
# 0. NECESSARY LIBRARY
#-----------------------------------------------------------------------

import pandas as pd
import numpy as np
import pyodbc
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score



#-----------------------------------------------------------------------
# 1. (I) DATA PROCESSING MODULE CONNECTION
#    (II) GUI MODULE CONNECTION
# Needs to connect local or remote SQL Database here
# Also, needs to GUI Module Connection here
# (**NOT UPDATED - NEEDS TO BE CHANGED)
#-----------------------------------------------------------------------

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



# Database Preprocessing
cursor = connect()

tableNames = ['schools', 'classes', 'resources', 'students', 'teachers']
keys = ['SchoolID', 'ClassID', 'ResourceID', 'StudentID', 'TeacherID']

frames = getFrames(tableNames, cursor)

while len(keys) > 1:
    framesToMerge = idFramesToMerge(frames, keys)
    mergeFrames(frames, keys, framesToMerge)





#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------
# 2. DATA ANALYSIS MODULE
# Backend part of the software application
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
# INPUTS FROM GUI:
# 1) Feature Selection (2 or 3)
# 2) Regression Type - Linear Regression, Ridge Regression, Lasso Regression, Gradient Boosting, Neural Network if time permits
# 3) Threshold - property, logic operator, text values
# 4) Excel (.csv) Option
#
# (**NEEDS TO THINK ABOUT HOW TO GET INPUTS FROM GUI MODULE)
# (**NOT UPDATED - NEEDS TO BE CHANGED)
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
# OUTPUTS TO GUI:
# 1) Visualization (2D or 3D)
# 2) Indicators - R^2, y-intercept, MSE, Cross Validation (CV)
# 3) Optional .csv
#
# (**NEEDS TO THINK ABOUT HOW TO SEND OUTPUTS TO GUI MODULE)
# (**NOT UPDATED - NEEDS TO BE CHANGED)
#-----------------------------------------------------------------------

dataset = frames[0]      # original dataset

COLUMN = dataset.columns # column list for "dataset"
NUM_COLUMN = COLUMN.size # number of columns in "COLUMN"

print "Single Merged Dataset: \n"
print dataset, '\n'



def data_analysis_module_init():
    print "------------------ initializing data analysis module... ------------------"
    # data processing module connection
    # dataset initialization
    # + anything that requires
    print "------------------ initializing done ------------------"



def data_analysis_module_linear_regression(feature1, feature2, y_intercept, r_squared):
    print "------------------ Linear Regression ------------------"
    # make sure:
    # feature1 - string
    # feature2 - string
    # y_intercept - boolean
    # rsquared - boolearn
    
    print "\n" + feature1 + " vs. " + feature2
    
    # 1. get filtered two features (needs to provide more threshold options)
    mean_x = np.mean(dataset[feature1])
    mean_y = np.mean(dataset[feature2])
    # first feature
    for k in range(0, len(dataset[feature1])):
        if dataset[feature1][k] < threshold:
            dataset[feature1][k] = mean_x
    # second feature
    for k in range(0, len(dataset[feature2])):
        if dataset[feature2][k] < threshold:
            dataset[feature2][k] = mean_y

    # 2. linear regression
    train_x = dataset[feature1].reshape(-1, 1)
    train_y = dataset[feature2]

    linearRegression = linear_model.LinearRegression()
    linearRegression.fit(train_x, train_y)

    pred_y = linearRegression.predict(train_x)

    # 3. output visualization
    title = feature1 + " vs. " + feature2
    plt.title(title)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.scatter(train_x, train_y,  color='blue')
    plt.plot(train_x, pred_y, color='orange', linewidth=3)
    plt.show()
    
    # 4. output indicators
    # Model coefficient(s)
    print '\nCoefficients:', linearRegression.coef_
    # Mean squared error
    print 'MSE:', mean_squared_error(train_y, pred_y)
    # Variance score: 1 is perfect prediction
    print 'R^2:', r2_score(train_y, pred_y)
    print 'Y-intecept:', linearRegression.coef_
    print '\n\n'
    print "------------------ Linear Regression done ------------------\n"


def data_analysis_module_filtering(feature1, feature2, logic, theshold):
    # code goes here
    # error checking required
    # feature 1 & feature 2 should string type
    # logic should be one of the followings: >, <, >=, <=, !=. ==, contains, !contains
    # threshold should be one of the types: int, string







#-----------------IGNORE HERE--------------------
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








