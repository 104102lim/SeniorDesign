# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------
  DataAnalysis.py
  
  Data Analysis Module for BH Oil Characterization Software Applcation
  
  Author: Sungho Lim, Joey Gallardo
  Last Updated Date: 10/31/2018
-----------------------------------------------------------------------
"""

import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from DatabasePreprocessing import getData, getDescriptions


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
    
    # check whether we analyze connected features
    if type(dataset) == str: # error cccuring
        return dataset       # output string information
    
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
    print('\nRaw two features:')
    print(output[0])
    print('\nCoefficients:', output[1])
    print('Y-intecept:', output[2])
    print('R^2:', output[3])
    print("\n------------------ Linear Regression Done ------------------\n")
    return output


#-----------------------------------------------------------------------------------------------
# Function: filtering
# Public function to filter some data given a target feature given the information of set of features
# Inputs:   targetFeature, comparisonFutures, logics, thresholds, operators
#           - all features should have str type
#           - logic should be one of the followings:
#               * >, <, >=, <=, =. !=, contains, does not contain
#               * where >, <, >=, <=, =, !=: int, float threshold (and data type)
#               * where =. !=, contains, does not contain: str threshold (and data type)
#           - threshold should be one of the types:
#               * int, float, string
#           - operator should be one of the followings:
#               * AND, OR
#           *** Length of comparisonFeatures, logics, thresholds should be same with at most 6
#           *** Length of operators should be one less than length of comparisonFeatures
# Outputs:  filtered dataset
#           - Panda dataframes with original feature1 & filtered feature1
#           *** If output format is "str" it explains what type of error sending to GUI
#-----------------------------------------------------------------------------------------------
def filtering(targetFeature, comparisonFeatures, logics, thresholds, operators):
    print("------------------ Filtering ------------------")
    # input type checking
    if (type(targetFeature) != str):
        return ("Target feature should be str type\n")
    for i in range(0, len(comparisonFeatures)):
        if (type(comparisonFeatures[i]) != str):
            return ("Comparison feature(s) should be str type\n")
        
    if len(comparisonFeatures) != len(logics):
        return ("Number of comparison features and logics should be same\n")
    if len(comparisonFeatures) != len(thresholds):
        return ("Number of comparison features and thresholds should be same\n")
    if len(comparisonFeatures) != (len(operators) + 1):
        return ("Number of operators should be one less than number of comparison features\n")
    
    for i in range(0, len(logics)):
        if (logics[i] != ">" and logics[i] != "<" and logics[i] != ">=" and logics[i] != "<=" and
            logics[i] != "=" and logics[i] != "!=" and logics[i] != "Contains" and logics[i] != "Does Not Contain"):
            return ("logic value(s) error\n")
    for i in range(0, len(thresholds)):
        if (type(thresholds[i]) != int and type(thresholds[i]) != float and type(thresholds[i]) != str):
            return ("threshold(s) should be int, float, or str type\n")
    for i in range(0, len(operators)):
        if (operators[i] != "AND" and operators[i] != "OR"):
            return ("operator(s) should be 'AND' or 'OR'\n")
    
    # get length
    length = len(comparisonFeatures)
    
    # get dataset
    allFeatureNames = []
    allFeatureNames.append(targetFeature)
    for i in range (0, length):
        allFeatureNames.append(comparisonFeatures[i])
    dataset = getData(allFeatureNames)
    
    # check whether we analyze connected features
    if type(dataset) == str: # error cccuring
        return dataset       # output string information
    
    new_targetfs = []
    new_targetfs_idx = []
    
    # filter target feature given comparison features
    for i in range(0, length):
        # check whether threshold and comparison feature are compatible
        checkError = __thresholdAndFeatureErrorCheckingForFiltering(comparisonFeatures[i], dataset[comparisonFeatures[i]], thresholds[i])
        if checkError != None: # error cccuring
            return checkError  # output string information
        
        # get data
        targetf = dataset[targetFeature]
        comparisonf = dataset[comparisonFeatures[i]]
        new_targetf = []
        new_targetf_idx = []
           
        # do filtering for target feature
        if logics[i] == '>':
            for j in range(0, len(targetf)):
                if (comparisonf[j] > thresholds[i]):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
        elif logics[i] == '<':
            for j in range(0, len(targetf)):
                if (comparisonf[j] < thresholds[i]):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
        elif logics[i] == '>=':
            for j in range(0, len(targetf)):
                if (comparisonf[j] >= thresholds[i]):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
        elif logics[i] == '<=':
            for j in range(0, len(targetf)):
                if (comparisonf[j] <= thresholds[i]):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
        elif logics[i] == '=':
            for j in range(0, len(targetf)):
                if (type(comparisonf[j]) == str and type(thresholds[i]) == str and comparisonf[j].lower() == thresholds[i].lower()):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
                elif (type(comparisonf[j]) != str and type(thresholds[i]) != str and comparisonf[j] == thresholds[i]):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
        elif logics[i] == '!=':
            for j in range(0, len(targetf)):
                if (type(comparisonf[j]) == str and type(thresholds[i]) == str and comparisonf[j].lower() != thresholds[i].lower()):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
                elif (type(comparisonf[j]) != str and type(thresholds[i]) != str and comparisonf[j] != thresholds[i]):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
        elif logics[i] == 'Contains':
            for j in range(0, len(targetf)):
                if (type(comparisonf[j]) == str and type(thresholds[i]) == str and thresholds[i].lower() in comparisonf[j].lower()):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
        elif logics[i] == 'Does Not Contain':
            for j in range(0, len(targetf)):
                if (type(comparisonf[j]) == str and type(thresholds[i]) == str and thresholds[i].lower() not in comparisonf[j].lower()):
                    new_targetf.append(targetf[j])
                    new_targetf_idx.append(j)
        
        # append the new target feature to the set of new target features
        new_targetfs.append(new_targetf)
        new_targetfs_idx.append(new_targetf_idx)
    
    
    # compose all filtered target features for the result
    result = new_targetfs[0]
    result_idx = new_targetfs_idx[0]
    new_result = []
    new_result_idx = []
    for i in range(0,length-1): # compare new_targetfs[i+1] and result
        if operators[i] == "AND":
            new_result = []
            new_result_idx = []
            for j in range(0,len(result_idx)):
                if result_idx[j] in new_targetfs_idx[i+1]:
                    new_result.append(result[j])
                    new_result_idx.append(j)
            result = new_result
            result_idx = new_result_idx
        elif operators[i] == "OR":
            for j in range(0,len(new_targetfs_idx[i+1])):
                if new_targetfs_idx[i+1][j] not in result_idx:
                    result.append(new_targetfs[i+1][j])
                    result_idx.append(j)

    # create new dataframe for output
    targetf = pd.DataFrame(data={targetFeature : dataset[targetFeature]})
    result = {targetFeature : result}
    result = pd.DataFrame(data=result)
    output = [targetf, result]
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
    # input type checking
    if (type(feature1) != str or type(feature2) != str):
        return ("feature(s) should be str type\n")
    print("\n" + feature1 + " vs. " + feature2)

    dataset = getData([feature1, feature2])
    
    # check whether we analyze connected features
    if type(dataset) == str: # error occuring
        return dataset       # output string information
    
    # check whether the features compatible
    checkError = __featureErrorCheckingForRegression(dataset)
    if checkError != None: # error occuring
        return checkError  # output string information
    
    X = np.array(dataset[feature1].values).reshape(-1, 1)
    y = np.array(dataset[feature2].values).reshape(-1, 1)
    poly = PolynomialFeatures(degree=order)
    poly_features = poly.fit_transform(X)
    poly_regression = linear_model.LinearRegression()
    poly_fit = poly_regression.fit(poly_features, y)
    coefs = poly_fit.coef_.copy()
    coefs[0, 0] = poly_fit.intercept_[0]
    return [dataset, coefs]


# check whether features compatible
# data should be numeric values for regressions
# feature1 & feature2
def __featureErrorCheckingForRegression(dataset):
    if len(dataset.columns) == 1:
        return ("Same features cannot be modeled.\n")
    f1 = dataset[dataset.columns[0]].values.tolist()
    f2 = dataset[dataset.columns[1]].values.tolist()
    for i in range(0, len(f1)):
        if type(f1[i]) != int and type(f1[i]) != float:
            return (dataset.columns[0] + " has non-numerical data type.\n")
    for i in range(0, len(f2)):
        if type(f2[i]) != int and type(f2[i]) != float:
            return (dataset.columns[1] + " has non-numerical data type.\n")
    return None

# check whether second feature and threshold compatible
# second feature and threshold should have same data type
# for example, str & str or numeric & numeric
def __thresholdAndFeatureErrorCheckingForFiltering(f2_name, f2, threshold):
    f2 = f2.values.tolist()
    if type(threshold) == str: # str compatible check
        for i in range(0, len(f2)):
            if type(f2[i]) != str:
                return ("Threshold " + threshold + " is string, but some of data in " + f2_name + " are not string.\n")
    else: # numeric compatible check
        for i in range(0, len(f2)):
            if type(f2[i]) != int and type(f2[i]) != float:
                return ("Threshold " + threshold + " is numeric, but some of data in " + f2_name + " are not numeric.\n")
    return None
