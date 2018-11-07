from __future__ import unicode_literals
import sys
import os
import matplotlib
import numpy as np
import pandas as pd

from numpy import arange, sin, pi

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QPushButton, QCheckBox
from PyQt5.QtWidgets import QScrollArea, QTableWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QWidget
from PyQt5.QtWidgets import QFileDialog, QCompleter


matplotlib.use('Qt5Agg')

progname = os.path.basename(sys.argv[0])
progversion = "0.1"
            


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Polynomial Regression'
        self.left = 500
        self.top = 100
        self.width = 600
        self.height = 100
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())

        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        self.featureX = QComboBox(self)
        self.featureX.setToolTip('Select feature for X axis')
        self.featureX.move(50, 20)
        self.featureX.resize(100, 20)
        label = QLabel('X-Axis Feature', self)
        label.move(50, 30)
        label.resize(100, 50)
        self.featureY = QComboBox(self)
        self.featureY.setToolTip('Select feature for Y axis')
        self.featureY.move(200, 20)
        self.featureY.resize(100, 20)
        label = QLabel('Y-Axis Feature', self)
        label.move(200, 30)
        label.resize(100, 50)
#         descriptions = getDescriptions()
#         descriptions = [d.lower() for d in descriptions]
#         descriptions.sort()
        self.featureX.setInsertPolicy(QComboBox.NoInsert)
        self.featureX.setEditable(True)
        self.featureX.setCompleter(QCompleter())
        self.featureX.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.featureY.setInsertPolicy(QComboBox.NoInsert)
        self.featureY.setEditable(True)
        self.featureY.setCompleter(QCompleter())
        self.featureY.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.order = QComboBox(self)
        self.order.setToolTip('Select order of polynomial fit')
        self.order.move(350, 20)
        label = QLabel('Order of Polynomial', self)
        label.move(350, 50)
        label.resize(150, 50)
        for i in range(1, 10):
            self.order.addItem(str(i))
#         descriptions = getDescriptions()
#         descriptions.sort()
#         for d in descriptions:
#             if (d != "bottom depth"
#                     and d != "top depth"
#                     and d != "Cost per unit"
#                     and d != "Name of mud engineer"): continue
#             self.featureY.addItem(d)
#             self.featureX.addItem(d)
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot poly regression')
#         plotButton.clicked.connect(self.parent().plotPolyRegression)
        plotButton.move(500, 20)
        plotButton.resize(50, 50)

if __name__ == '__main__':
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("Analysis Toolkit Prototype")
    aw.show()
    sys.exit(qApp.exec_())
