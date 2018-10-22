# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------
  DataAnalysisModule.py
  
  Data Analysis Module for BH Oil Characterization Software Applcation
  
  Author: Sungho Lim, Joey Gallardo
  Last Updated Date: 09/28/2018
-----------------------------------------------------------------------
"""


import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from DatabasePreprocessing import getData, getDescriptions


#-----------------------------------------------------------------------------------------------
#                       DATA ANALYSIS MODULE
#
# Backend parts of the software application for GUI Module
#
# INPUTS FROM GUI:
# 1) Analysis Type - Linear Regression, Polynomial Regression, or Filtering
# 2) Feature Names (2 or 3)
# 3) Threshold - logic operator, threshold
#
# OUTPUTS TO GUI:
# 1) Indicators - (filtered or raw) Datasets, Coefficents, R^2, y-intercept
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
# Function: __testInialization__
# Private function for testing public methods
#-----------------------------------------------------------------------------------------------
def __testInialization__(self):
    data = [[3,'ha',0,5,4], [23,'he',8,9,10], [2,'hi',6,7,1], [0,'ho',2,5,-2],
            [5,'hu',13,14,15], [0,'ohio',4,3,5], [8,'hello',18,19,20], [-2,'hike',-3,-8,9],
            [21,'hamony',23,24,25], [-9,'hihihio',-13,-14,-15]]
    cols = ["Feature1","Feature2","Feature3","Feature4","Feature5"]

    ds = pd.DataFrame(data, columns=cols, dtype=float)  # test dataframe
    dataset = ds
    print("Test Dataset Initialized")

#-----------------------------------------------------------------------------------------------
# Function: linearRegression
# Public function to do linear regression given existing two feature string inputs
# Inputs:   string names of two feature
# Outputs:  raw datasets, coefficients of linear regression,
#           y-intercept, r^2
#           *** If output format is "str" it explains what type of error sending to GUI
#-----------------------------------------------------------------------------------------------
def linearRegression(feature1, feature2):
    print("------------------ Linear Regression ------------------")
    # input type checking
    if (type(feature1) != str or type(feature2) != str):
        return ("feature(s) should be str type\n")
    print("\n" + feature1 + " vs. " + feature2)

    # retrieve dataset
    dataset = getData([feature1, feature2])  
    
    # check whether the features compatible
    checkError = __featureErrorCheckingForRegression(dataset)
    if checkError != None: # error occuring
        return checkError  # output string information
    
    # 1. linear regression
    train_x = dataset[feature1].values.reshape(-1, 1)
    train_y = dataset[feature2]

    linearRegression = linear_model.LinearRegression()
    linearRegression.fit(train_x, train_y)

    pred_y = linearRegression.predict(train_x)

    # 2. output indicators
    # Features
    rawDataSet = {feature1 : dataset[feature1], feature2 : dataset[feature2]}
    rawDataFrame = pd.DataFrame(data=rawDataSet)

    output = [rawDataFrame, linearRegression.coef_,
                     linearRegression.intercept_, r2_score(train_y, pred_y)]

    print('\nRaw features:')
    print(output[0])
    print('\nCoefficients:', output[1])
    print('Y-intecept:', output[2])
    print('R^2:', output[3])
    print("\n------------------ Linear Regression Done ------------------\n")
    return output


#-----------------------------------------------------------------------------------------------
# Function: filtering
# Public function to do filtering the second feature given existing two feature string inputs
# Inputs:   string names of two feature, logic, and threshold
#           - feature 1 & feature 2 should str type
#           - logic should be one of the followings:
#               * >, <, >=, <=, =. !=, contains, does not contain
#               * where >, <, >=, <=, =, !=: int, float threshold (and data type)
#               * where =. !=, contains, does not contain: str threshold (and data type)
#           - threshold should be one of the types:
#               * int, float, string
# Outputs:  filtered dataset
#           - Panda dataframes with original feature1 & filtered feature1
#           *** If output format is "str" it explains what type of error sending to GUI
#-----------------------------------------------------------------------------------------------
def filtering(feature1, feature2, logic, threshold):
    print("------------------ Filtering ------------------")
    # input type checking
    if (type(feature1) != str or type(feature2) != str):
        return ("feature(s) should be str type\n")
    if (logic != ">" and logic != "<" and logic != ">=" and logic != "<=" and
        logic != "=" and logic != "!=" and logic != "contains" and logic != "does not contain"):
        return ("logic value error\n")
    if (type(threshold) != int and type(threshold) != float and type(threshold) != complex and type(threshold) != str):
        return ("threshold should be int, float, or str type\n")
        
    # retrieve dataset
    dataset = getData([feature1, feature2])
    
    # check whether threshold and second feature are compatible
    checkError = __thresholdAndFeatureErrorCheckingForFiltering(dataset, threshold)
    if checkError != None:
        return checkError

    # f1.size & f2.size should be same
    # get data from feature2
    f1 = dataset[feature1]
    f2 = dataset[feature2]
    new_f1 = []

    # do filtering for feature2
    # ex) (type(f2[i]) == int or type(f2[i]) == long) and (type(threshold) == int or type(threshold) == float)
    if logic == '>':
        for i in range(0, len(f1)):
            if (f2[i] > threshold):
                new_f1.append(f1[i])
    elif logic == '<':
        for i in range(0, len(f1)):
            if (f2[i] < threshold):
                new_f1.append(f1[i])
    elif logic == '>=':
        for i in range(0, len(f1)):
            if (f2[i] >= threshold):
                new_f1.append(f1[i])
    elif logic == '<=':
        for i in range(0, len(f1)):
            if (f2[i] <= threshold):
                new_f1.append(f1[i])
    elif logic == '=':
        for i in range(0, len(f1)):
            if (type(f2[i]) == str and type(threshold) == str and f2[i] == threshold):
                new_f1.append(f1[i])
            elif (f2[i] == threshold):
                new_f1.append(f1[i])
    elif logic == '!=':
        for i in range(0, len(f1)):
            if (type(f2[i]) == str and type(threshold) == str and f2[i] != threshold):
                new_f1.append(f1[i])
            elif (f2[i] != threshold):
                new_f1.append(f1[i])
    elif logic == 'contains':
        for i in range(0, len(f1)):
            if (type(f2[i]) == str and type(threshold) == str):
                if (threshold in f2[i]):
                    new_f1.append(f1[i])
    elif logic == 'does not contain':
        for i in range(0, len(f1)):
            if (type(f2[i]) == str and type(threshold) == str):
                if (threshold not in f2[i]):
                    new_f1.append(f1[i])

    # create new dataframe for output
    f1 = pd.DataFrame(data={feature1 : dataset[feature1]})
    new_f1 = {feature1 : new_f1}
    new_f1 = pd.DataFrame(data=new_f1)
    output = [f1, new_f1]
    print("First feature:")
    print(output[0])
    print("Filtered first feature:")
    print(output[1])
    print("------------------ Filtering Done ------------------\n")
    return output

#-----------------------------------------------------------------------------------------------
# Function: polynomialRegression
# Public function to do polynomial regression given existing two feature string inputs
# Inputs:   string names of two feature
# Outputs:  raw datasets, coefficients of ploynomial regression,
#           y-intercept, r^2 (?)
#-----------------------------------------------------------------------------------------------
def polynomialRegression(feature1, feature2, order):
    
    if (type(feature1) != str or type(feature2) != str):
        return ("feature(s) should be str type\n")
    print("\n" + feature1 + " vs. " + feature2)

    dataset = getData([feature1, feature2])
    checkError = __featureErrorCheckingForRegression(dataset)
    if checkError != None: # error occuring
        return checkError  # output string information
    
    X = np.array(dataset[feature1].values).reshape(-1, 1)
    y = np.array(dataset[feature2].values).reshape(-1, 1)
    poly = PolynomialFeatures(degree=order)
    poly_features = poly.fit_transform(X)
    poly_regression = linear_model.LinearRegression()
    poly_fit = poly_regression.fit(poly_features, y)
    return [dataset, poly_fit.coef_]




# check whether features compatible
# data should be numerical values for regressions
# feature1 & feature2
def __featureErrorCheckingForRegression(dataset):
    if len(dataset.columns) == 1:
        return ("Same feature(s) cannot be modeled.\n")
    f1 = dataset[dataset.columns[0]].values
    f2 = dataset[dataset.columns[1]].values
    for i in range(0, len(f1)):
        if type(f1[i]) == str:
            return (dataset.columns[0] + " has non-numerical data type.\n")
        elif type(f1[i].item()) != int and type(f1[i].item()) != float and type(f1[i].item()) != complex:
            return (dataset.columns[0] + " has non-numerical data type.\n")
    for i in range(0, len(f2)):
        if type(f2[i]) == str:
            return (dataset.columns[1] + " has non-numerical data type.\n")
        elif type(f2[i].item()) != int and type(f2[i].item()) != float and type(f2[i].item()) != complex:
            return (dataset.columns[1] + " has non-numerical data type.\n")
    return None

# check whether second feature and threshold compatible
# second feature and threshold should have same data type
# for example, str & str, int & int, float & float, complex & complex
def __thresholdAndFeatureErrorCheckingForFiltering(dataset, threshold):
    idx = 1
    if len(dataset.columns) == 1:
        idx = 0
    f2 = dataset[dataset.columns[idx]].values
    if type(threshold) == str: # str compatible check
        for i in range(0, len(f2)):
            if type(f2[i]) != str:
                return ("Threshold is string, but some of data in " + dataset.columns[idx] + " are not string.\n")
    else: # numeric compatible check
        for i in range(0, len(f2)):
            if type(f2[i].item()) != int and type(f2[i].item()) != float and type(f2[i].item()) != complex:
                return ("Threshold is numeric, but some of data in " + dataset.columns[idx] + " are not numeric.\n")
    return None
