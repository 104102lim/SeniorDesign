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
class DataAnalysis():
    #-----------------------------------------------------------------------------------------------
    # Function: __init__
    # Private function for constructor of DataAnalysis object
    #-----------------------------------------------------------------------------------------------
    def __init__(self):
        self.dataset = pd.DataFrame() # raw dataset
        print "Data Analysis Module Initialized"
    
    
    #-----------------------------------------------------------------------------------------------
    # Function: __testInialization__
    # Private function for testing public methods
    #-----------------------------------------------------------------------------------------------
    def __testInialization__(self):
        data = [[3,2,0,5,4], [23,7,8,9,10], [2,3,6,7,1], [0,9,2,5,-2], [5,7,13,14,15], [0,5,4,3,5], [8,-5,18,19,20], [-2,2,-3,-8,9], [21,9,23,24,25], [-9,-7,-13,-14,-15]]
        cols = ["Feature1","Feature2","Feature3","Feature4","Feature5"]

        ds = pd.DataFrame(data, columns=cols, dtype=float)  # test dataframe
        self.dataset = ds
        print "Test Dataset Initialized"
    
    
    #-----------------------------------------------------------------------------------------------
    # Function: __printDataset__
    # Private function for printing out dataset
    #-----------------------------------------------------------------------------------------------
    def __printDataset__(self):
        print "Current Dataset: \n"
        print self.dataset, '\n'
    
    
    #-----------------------------------------------------------------------------------------------
    # Function: dataprocessingConnect
    # Public function to connect Data Processing Module and get raw dataset
    # (*** NOT UPDATED - NEEDS TO BE CHANGED)
    #-----------------------------------------------------------------------------------------------
    def dataprocessingConnect(self):
        print "------------------ Connecting Data Processing Module ------------------"
        # data processing module connection
        # dataset initialization
        # + anything that requires
        
        print "------------------ Connection Done ------------------"
    
    
    #-----------------------------------------------------------------------------------------------
    # Function: linearRegression
    # Public function to do linear regression given existing two feature string inputs
    # Inputs:   string names of two feature
    # Outputs:  raw datasets, coefficients of linear regression,
    #           y-intercept, r^2
    #-----------------------------------------------------------------------------------------------
    def linearRegression(self, feature1, feature2):
        print "------------------ Linear Regression ------------------"
    
        # input type checking
        if (type(feature1) != str or type(feature2) != str):
            print "feature(s) should be str type\n"
            return 0

        print "\n" + feature1 + " vs. " + feature2
       
        # 1. linear regression
        train_x = self.dataset[feature1].reshape(-1, 1)
        train_y = self.dataset[feature2]

        linearRegression = linear_model.LinearRegression()
        linearRegression.fit(train_x, train_y)

        pred_y = linearRegression.predict(train_x)

        # visualization - for test only
        #title = feature1 + " vs. " + feature2
        #plt.title(title)
        #plt.xlabel(feature1)
        #plt.ylabel(feature2)
        #plt.scatter(train_x, train_y,  color='blue')
        #plt.plot(train_x, pred_y, color='orange', linewidth=3)
        #plt.show()

        # 2. output indicators
        # Features
        rawDataSet = {feature1 : self.dataset[feature1], feature2 : self.dataset[feature2]}
        rawDataFrame = pd.DataFrame(data=rawDataSet)
    
        # output the package for GUI Module
        # output[0] = rawDataFrame
        # output[1] = coefficient of linear model
        # output[2] = Y_intercept
        # output[3] = R^2
        output = [rawDataFrame, linearRegression.coef_, 
                         linearRegression.intercept_, r2_score(train_y, pred_y)]
    
        print '\nRaw features:'
        print output[0]
        print '\nCoefficients:', output[1]
        print 'Y-intecept:', output[2]
        print 'R^2:', output[3]
        print "\n------------------ Linear Regression Done ------------------\n"
        return output
    
    
    #-----------------------------------------------------------------------------------------------
    # Function: filtering
    # Public function to do filtering the second feature given existing two feature string inputs
    # Inputs:   string names of two feature, logic, and threshold
    #           - feature 1 & feature 2 should str type
    #           - logic should be one of the followings: 
    #               * >, <, >=, <=, ==. !=, contains, !contains
    #               * where >, <, >=, <=, ==, !=: int, float threshold (and data type)
    #               * where ==. !=, contains, !contains: str threshold (and data type)
    #           - threshold should be one of the types: 
    #               * int, float, string
    # Outputs:  filtered dataset
    #           - a Panda dataframe with original feature1 & filtered feature2
    #           Error codes for non-matching data types
    #           - return 0: feature type error
    #           - return -1: logic type error
    #           - return -2: threshold type error
    #-----------------------------------------------------------------------------------------------
    def filtering(self, feature1, feature2, logic, threshold):
        print "------------------ Filtering ------------------"
    
        # input type checking
        if (type(feature1) != str or type(feature2) != str):
            print "feature(s) should be str type\n"
            return 0
        if (logic != ">" and logic != "<" and logic != ">=" and logic != "<=" and
            logic != "==" and logic != "!=" and logic != "contains" and logic != "!contains"):
            print "logic value error\n"
            return -1
        if (type(threshold) != int and type(threshold) != float and type(threshold) != str):
            print "threshold should be int, float, or str type\n"
            return -2
    
        # f1.size & f2.size should be same
        # get data from feature2
        f1 = self.dataset[feature1]
        f2 = self.dataset[feature2]
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
        elif logic == '==':
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
        elif logic == '!contains':
            for i in range(0, len(f1)):
                if (type(f2[i]) == str and type(threshold) == str):
                    if (threshold not in f2[i]):
                        new_f1.append(f1[i])
   
        # create new dataframe for output
        f1 = pd.DataFrame(data={feature1 : self.dataset[feature1]})
        new_f1 = {feature1 : new_f1}
        new_f1 = pd.DataFrame(data=new_f1)
        
        # output the package for GUI Module
        # output[0] = feature1 pandas dataset
        # output[1] = filtered feature2 pandas dataset
        output = [f1, new_f1]
        
        
        print "First feature:"
        print output[0]
        print "Filtered first feature:"
        print output[1]
        print "------------------ Filtering Done ------------------\n"
        return output
    
    
    #-----------------------------------------------------------------------------------------------
    # Function: polynomialRegression
    # Public function to do polynomial regression given existing two feature string inputs
    # Inputs:   string names of two feature
    # Outputs:  raw datasets, coefficients of ploynomial regression,
    #           y-intercept, r^2 (?)
    #-----------------------------------------------------------------------------------------------
    def polynomialRegression(self, feature1, feature2):  
        # Implementation goes here
        return 0






