import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

data = [[1,2,3,4,5], [23,7,8,9,10], [5,7,13,14,15], [8,-5,18,19,20], [21,9,23,24,25]]
cols = ["Feature1","Feature2","Feature3","Feature4","Feature5"]

dataset = pd.DataFrame(data, columns=cols, dtype=float)  # original dataset

COLUMN = dataset.columns # column list for "dataset"
NUM_COLUMN = COLUMN.size # number of columns in "COLUMN"

#print "Orginial Dataset: \n"
#print dataset, '\n'
X = dataset.iloc["Feature1"].values
y = dataset.iloc["Feature2"].values

M=2
poly_features=PolynomialFeatures(degree=M, include_bias=False)
#train_x = dataset["Feature1"].values.reshape(-1, 1)
#X_poly=poly_features.fit_transform(train_x)
#train_y = dataset["Feature2"]
linearRegression = linear_model.LinearRegression()
#linearRegression.fit(X_poly,train_y)
#pred_y = linearRegression.predict(X_poly)
newX = poly.fit_transform(X)






model=LinearRegression()
model.fit(X_poly,train_y) # Fit the model

# Plot
#X_plot=np.linspace(0,1,100).reshape(-1,1)
X#_plot_poly=poly_features.fit_transform(X_poly)
#plt.plot(train_x,train_y,"b.")
i=0
plt.plot(X_poly[:,i],model.predict(X_poly),'-r')
plt.show()
