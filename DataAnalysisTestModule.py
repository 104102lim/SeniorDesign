# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------
  DataAnalysisTestModule.py
    
  Test Module for Data Analysis Module of BH Oil Characterization Software Applcation
    
  Author: Sungho Lim, Joey Gallardo
  Last Updated Date: 09/28/2018
-----------------------------------------------------------------------
"""


import DataAnalysis as DA


# Initialization
#da = DA.DataAnalysis()
#da.__testInialization__()
#da.__printDataset__()


#------------ Simple Test 1 ------------
# *** Please refer to "testInialization" for the feature name(s)
#linearRegressionOutput = DA.linearRegression('Feature1', 'Feature2')


filteringOutput = DA.filtering2("Feature5", "Feature5", ">=", 0)
#filteringOutput = DA.filtering("Feature5", ["Feature5"], [">="], [0], [])
#filteringOutput = DA.filtering("Feature5", ["Feature5", "Feature5"], [">=", "<="], [0, 5], ["AND"])
#filteringOutput = DA.filtering("Feature5", ["Feature5", "Feature5"], [">=", "<="], [0, 3], ["OR"])
#filteringOutput = DA.filtering("Feature5", ["Feature5", "Feature5", "Feature5"], [">=", "<=", "<="], [0, 5, 3], ["AND", "AND"])
#filteringOutput = DA.filtering("Feature5", ["Feature5", "Feature5", "Feature5","Feature5","Feature5","Feature5"], ["<=", "<=", "<=","<=","<=","<="], [10, 9, 8,7,6,5], ["AND", "AND","AND", "AND","AND"])



# 1. output of linearRegression
#if type(linearRegressionOutput) == str:
#    print (linearRegressionOutput)
#print (linearRegressionOutput[0])
#print ('\nCoefficients:', linearRegressionOutput[1])
#print ('Y-intecept:', linearRegressionOutput[2])
#print ('R^2:', linearRegressionOutput[3])

# 2. output of filtering
if type(filteringOutput) == str:
    print (filteringOutput)
print ("\nFirst feature:")
print (filteringOutput[0])
print ("\nFiltered first feature:")
print (filteringOutput[1])



#data_analysis_module_linear_regression(cols[0], cols[1])
#data_analysis_module_linear_regression(cols[1], cols[2])
#data_analysis_module_linear_regression(cols[2], cols[3])
#data_analysis_module_linear_regression(cols[3], cols[4])
#data_analysis_module_linear_regression(cols[0], cols[2])
#data_analysis_module_linear_regression(cols[0], cols[3])

#data_analysis_module_filtering(cols[0], cols[1], '>', 0)
