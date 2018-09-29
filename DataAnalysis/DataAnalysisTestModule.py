# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------------
  DataAnalysisTestModule.py
    
  Test Module for Data Analysis Module of BH Oil Characterization Software Applcation
    
  Author: Sungho Lim, Joey Gallardo
  Last Updated Date: 09/28/2018
-----------------------------------------------------------------------
"""


import DataAnalysisModule as DA


# Initialization
da = DA.DataAnalysis()
da.__testInialization__()
da.__printDataset__()


#------------ Simple Test 1 ------------
# *** Please refer to "testInialization" for the feature name(s)
linearRegressionOutput = da.linearRegression('Feature1', 'Feature2')
filteringOutput = da.filtering('Feature1', 'Feature2', '>', 0)

# 1. output of linearRegression
print linearRegressionOutput[0]
print '\nCoefficients:', linearRegressionOutput[1]
print 'Y-intecept:', linearRegressionOutput[2]
print 'R^2:', linearRegressionOutput[3]

# 2. output of filtering
print "\nFirst feature:"
print filteringOutput[0]
print "\nFiltered second feature:"
print filteringOutput[1]



#data_analysis_module_linear_regression(cols[0], cols[1])
#data_analysis_module_linear_regression(cols[1], cols[2])
#data_analysis_module_linear_regression(cols[2], cols[3])
#data_analysis_module_linear_regression(cols[3], cols[4])
#data_analysis_module_linear_regression(cols[0], cols[2])
#data_analysis_module_linear_regression(cols[0], cols[3])

#data_analysis_module_filtering(cols[0], cols[1], '>', 0)

