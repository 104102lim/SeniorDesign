from __future__ import unicode_literals
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import QtWidgets

class plottingCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def clear_figure(self):
        self.axes.cla()
        self.draw()

    def update_figure(self, data, Xlabel, Ylabel, Linear=False, Poly=False, yint=False, slope=False, rsquare=False):
        sData = data[0]
        sX = sData[Xlabel].tolist()
        sY = sData[Ylabel].tolist()

        xmin = min(sX)
        xmax = max(sX)
        length = xmax - xmin
        plus = length / 10
        xmin = xmin - plus
        xmax = xmax + plus
        interval = (xmax - xmin) / 1000
        X = np.arange(xmin, xmax, interval)

        if (Linear):
            slope_hat = data[1]
            yint_hat = data[2]
            Y = slope_hat * X + yint_hat

            yintTxt = "Y-int: "
            slopTxt = "Slope: "
            rsquareTxt = "R^2: "
            txt = ""

            if (yint):
                txt = txt + yintTxt + str(data[2])

            if (slope):
                txt = txt + "\n" + slopTxt + str(data[1])

            if (rsquare):
                txt = txt + "\n" + rsquareTxt + str(data[3])

            self.axes.cla()
            self.axes.scatter(sX, sY, color='green')
            self.axes.plot(X, Y, color='red')
            self.axes.set_xlabel(xlabel=Xlabel)
            self.axes.set_ylabel(ylabel=Ylabel)
            self.axes.set_title("Linear Regression: " + Ylabel + " vs. " + Xlabel)
            self.axes.legend(loc='best', title=txt)

        if (Poly):
            Y = []
            for i in range(len(X)):
                Y.append(self.PolyCoefficients(X[i], data[1][0]))

            txt = "Order: " + str(len(data[1][0]) - 1)
            self.axes.cla()
            self.axes.scatter(sX, sY, color='green')
            self.axes.plot(X, Y, color='red')
            self.axes.set_xlabel(xlabel=Xlabel)
            self.axes.set_ylabel(ylabel=Ylabel)
            self.axes.set_title("Polynomial Regression: " + Ylabel + " vs. " + Xlabel)
            self.axes.legend(loc='best', title=txt)

        self.draw()

    def PolyCoefficients(self, x, coeffs):
        """ Returns a polynomial for ``x`` values for the ``coeffs`` provided.

        The coefficients must be in ascending order (``x**0`` to ``x**o``).
        """
        o = len(coeffs)
        # print('# This is a polynomial of order {ord}.')
        y = 0
        for i in range(o):
            y += coeffs[i] * (x ** i)
        return y