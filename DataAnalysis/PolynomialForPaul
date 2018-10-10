#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 12:23:12 2018

@author: JoeyGallardo
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
from sklearn.linear_model import LinearRegression
#loading the dataset

data = [[1,2,3,4,5], [23,7,8,9,10], [5,7,13,14,15], [8,-5,18,19,20], [21,9,23,24,25]]
cols = ["Feature1","Feature2","Feature3","Feature4","Feature5"]

dataset = pd.DataFrame(data, columns=cols, dtype=float)  # original dataset

COLUMN = dataset.columns # column list for "dataset"
NUM_COLUMN = COLUMN.size # number of columns in "COLUMN"




X = dataset.iloc[:, 1:2].values
y = dataset.iloc[:, 2].values

#adding Polynomial for better fitting of data 
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree= 2)
poly_features = poly.fit_transform(X)

poly_regression = LinearRegression()
poly_regression.fit(poly_features,y)



plt.scatter(X, y, color = 'red')
plt.plot(X,poly_regression.predict(poly_features), color = 'blue')
plt.title('Does this work')
plt.xlabel('This shit is here')
plt.ylabel('Please work')
plt.show()

#ploting the data  
#i=0
#plt.plot(poly_features[:,i],poly_regression.predict(poly_features),'-r')
#plt.show()
