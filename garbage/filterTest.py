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
from PyQt5.QtWidgets import QFileDialog


matplotlib.use('Qt5Agg')

progname = os.path.basename(sys.argv[0])
progversion = "0.1"
            


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Filter Data'
        self.left = 500
        self.top = 50
        self.width = 400
        self.height = 400
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

        self.counter = 0
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.vLayout = QVBoxLayout(self.centralWidget)

        self.buttonsWidget = []
        self.buttonsWidgetLayout = []
        self.threshold = []
        self.feature1 = []
        self.feature2 = []
        self.logic = []
        for i in range(6):
            self.buttonsWidget.append(QWidget())
            self.buttonsWidgetLayout.append(QHBoxLayout(self.buttonsWidget[i]))
            self.threshold.append(QLineEdit(self))
            self.logic.append(QComboBox(self))
            self.feature1.append(QComboBox(self))
            self.feature2.append(QComboBox(self))
            if i > 0:
                self.threshold[i].hide()
                self.feature1[i].hide()
                self.feature2[i].hide()
                self.logic[i].hide()
        operators = ["AND", "OR"]
        for i in range(1, len(self.threshold)):
            for p in operators:
                self.feature1[i].addItem(p)
        logics = ["=", "!=", "<", ">", "<=", ">=", "Contains", "Does Not Contain"]
        for i in range(len(self.logic)):
            for l in logics:
                self.logic[i].addItem(l)
        self.addButton = QPushButton('+', self)
        self.addButton.clicked.connect(self.addExpression)
        filterButton = QPushButton('Filter', self)
        filterButton.move(300, 500)
        filterButton.setToolTip('Use button to filter the feature based on the chosen logic')
        self.label = QLabel('WHERE', self)

        for i in range(6):
            self.buttonsWidgetLayout[i].addWidget(self.feature1[i])
            self.buttonsWidgetLayout[i].addWidget(self.label)
            self.buttonsWidgetLayout[i].addWidget(self.feature2[i])
            self.buttonsWidgetLayout[i].addWidget(self.logic[i])
            self.buttonsWidgetLayout[i].addWidget(self.threshold[i])
            self.buttonsWidgetLayout[i].addWidget(self.addButton)
            self.buttonsWidgetLayout[i].addWidget(filterButton)
            self.vLayout.addWidget(self.buttonsWidget[i])
            #self.buttonsWidgetLayout[i].addSpacing(10)
    def addExpression(self):
        if(self.counter == 4):
            self.addButton.hide()
        if(self.counter < 5):
            self.counter += 1
            self.feature2[self.counter].show()
            self.feature1[self.counter].show()
            self.logic[self.counter].show()
            self.threshold[self.counter].show()  
        

if __name__ == '__main__':
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("Analysis Toolkit Prototype")
    aw.show()
    sys.exit(qApp.exec_())
