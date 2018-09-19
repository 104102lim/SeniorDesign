#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 20:39:23 2018

@author: liuxx
"""

import sys
import numpy as np
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random


class Window(QDialog):
    def __init__(self, parent = None):
        x = np.linspace(-1, 1, 50)
        y1 = 2 * x + 1
        y2 = x ** 2

        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.pbutton = QPushButton('Plot')
        self.pbutton.clicked.connect(lambda: self.plot(x, y1))

        self.lButton = QPushButton('Load')
        self.lButton.clicked.connect(lambda: self.load(x, y2))

        self.eButton = QPushButton('Exit')
        self.eButton.clicked.connect(self.exitButton)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.pbutton)
        layout.addWidget(self.lButton)
        layout.addWidget(self.eButton)
        self.setLayout(layout)

    def plot(self, x, y):
        ''' plot some random stuff '''
        # random data
        # data = [random.random() for i in range(10)]
        data = [x, y]

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data)

        # refresh canvas
        self.canvas.draw()

    def load(self, x, y):
        data = [x, y]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data)
        self.canvas.draw()

    def exitButton(self):
        QtCore.QCoreApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())