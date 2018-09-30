import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# generate N random points
N=30
X= np.random.rand(N,1)
y= np.sin(np.pi*2*X)+ np.random.randn(N,1)

M=9
poly_features=PolynomialFeatures(degree=M, include_bias=False)
X_poly=poly_features.fit_transform(X) # contain original X and its new features
model=LinearRegression()
model.fit(X_poly,y) # Fit the model

# Plot
X_plot=np.linspace(0,1,100).reshape(-1,1)
X_plot_poly=poly_features.fit_transform(X_plot)
plt.plot(X,y,"b.")
i=0
plt.plot(X_plot_poly[:,i],model.predict(X_plot_poly),'-r')
plt.show()
