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
        if (type(thresholds[i]) != int and type(thresholds[i]) != float and type(thresholds[i]) != complex and type(thresholds[i]) != str):
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



def filtering2(feature1, feature2, logic, threshold):
   print("------------------ Filtering ------------------")
   # input type checking
   if (type(feature1) != str or type(feature2) != str):
       return ("feature(s) should be str type\n")
   if (logic != ">" and logic != "<" and logic != ">=" and logic != "<=" and
       logic != "=" and logic != "!=" and logic != "Contains" and logic != "Does Not Contain"):
       return ("logic value error\n")
   if (type(threshold) != int and type(threshold) != float and type(threshold) != complex and type(threshold) != str):
       return ("threshold should be int, float, or str type\n")

   # retrieve dataset
   dataset = getData([feature1, feature2])
   
   # check whether we analyze connected features
   if type(dataset) == str: # error occuring
      return dataset        # output string information

   # check whether threshold and second feature are compatible
   checkError = __thresholdAndFeatureErrorCheckingForFiltering(feature2, dataset[feature2], threshold)
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
           if (type(f2[i]) == str and type(threshold) == str and f2[i].lower() == threshold.lower()):
               new_f1.append(f1[i])
           elif (f2[i] == threshold):
               new_f1.append(f1[i])
   elif logic == '!=':
       for i in range(0, len(f1)):
           if (type(f2[i]) == str and type(threshold) == str and f2[i].lower() != threshold.lower()):
               new_f1.append(f1[i])
           elif (f2[i] != threshold):
               new_f1.append(f1[i])
   elif logic == 'Contains':
       for i in range(0, len(f1)):
           if (type(f2[i]) == str and type(threshold) == str and threshold.lower() in f2[i].lower()):
               new_f1.append(f1[i])
   elif logic == 'Does Not Contain':
       for i in range(0, len(f1)):
           if (type(f2[i]) == str and type(threshold) == str and threshold.lower() not in f2[i].lower()):
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
# for example, str & str or numeric & numeric
def __thresholdAndFeatureErrorCheckingForFiltering(f2_name, f2, threshold):
    f2 = f2.values
    if type(threshold) == str: # str compatible check
        for i in range(0, len(f2)):
            if type(f2[i]) != str:
                return ("Threshold " + threshold + " is string, but some of data in " + f2_name + " are not string.\n")
    else: # numeric compatible check
        for i in range(0, len(f2)):
            if type(f2[i].item()) != int and type(f2[i].item()) != float and type(f2[i].item()) != complex:
                return ("Threshold " + threshold + " is numeric, but some of data in " + f2_name + " are not numeric.\n")
    return None

# private function for testing public methods
def __testInialization__(self):
    data = [[3,'ha',0,5,4], [23,'he',8,9,10], [2,'hi',6,7,1], [0,'ho',2,5,-2],
            [5,'hu',13,14,15], [0,'ohio',4,3,5], [8,'hello',18,19,20], [-2,'hike',-3,-8,9],
            [21,'hamony',23,24,25], [-9,'hihihio',-13,-14,-15]]
    cols = ["Feature1","Feature2","Feature3","Feature4","Feature5"]

    ds = pd.DataFrame(data, columns=cols, dtype=float)  # test dataframe
    dataset = ds
    print (dataset)
    print("Test Dataset Initialized")