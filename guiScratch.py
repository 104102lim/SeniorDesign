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


class filterDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(filterDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Filter Data'
        self.left = 500
        self.top = 50
        self.width = 800
        self.height = 300
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())

        self.counter = 0
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.vLayout = QVBoxLayout(self.centralWidget)

        
        self.bw1 = QWidget()
        self.bw2 = QWidget()
        self.bw3 = QWidget()
        self.buttonsWidgets = [self.bw1, self.bw2, self.bw3]
    
        self.bwl1 = QHBoxLayout(self.buttonsWidgets[0])
        self.bwl2 = QHBoxLayout(self.buttonsWidgets[0])
        self.bwl3 = QHBoxLayout(self.buttonsWidgets[0])
        self.buttonsWidgetLayout = [self.bwl1, self.bwl2, self.bwl3]
        
        self.feature1 = QComboBox(self)
        self.feature2 = QComboBox(self)
        self.logic = QComboBox(self)
        self.logic.setToolTip('Select logic')
        self.logic.addItem("=")
        self.logic.addItem("!=")
        self.logic.addItem("<")
        self.logic.addItem(">")
        self.logic.addItem("<=")
        self.logic.addItem(">=")
        self.logic.addItem("contains")
        self.logic.addItem("does not contain")
        self.threshold1 = QLineEdit(self)
        self.threshold2 = QLineEdit(self)
        self.threshold3 = QLineEdit(self)
        self.thresholds = [self.threshold1, self.threshold2, self.threshold3]
        addButton = QPushButton('+', self) 
        addButton.clicked.connect(self.addExpression)
        filterButton = QPushButton('Filter', self) 
        filterButton.setToolTip('Use button to filter the feature based on the chosen logic')
        filterButton.clicked.connect(self.filterData)
        
        self.buttonsWidgetLayout[0].addWidget(self.feature1)
        self.buttonsWidgetLayout[0].addWidget(self.feature2)
        self.buttonsWidgetLayout[0].addWidget(self.logic)
        self.buttonsWidgetLayout[0].addWidget(self.thresholds[0])
        self.buttonsWidgetLayout[0].addWidget(addButton)
        self.buttonsWidgetLayout[0].addWidget(filterButton)
        
        
        self.vLayout.addWidget(self.buttonsWidgets[0])
        
    def filterData(self):
            f1 = str(self.feature1.currentText())
            f2 = str(self.feature2.currentText())
            threshold1 = self.threshold1.text()
            threshold2 = self.threshold2.text()
            print("Processing")
            print(f1 + " " + f2 + " " + threshold1 + " " + threshold2)
            
    def addExpression(self):
        if(self.counter < 5):
            #self.vLayout.addWidget(self.feature1)
            self.feature1 = QComboBox(self)
            self.feature2 = QComboBox(self)
            self.logic = QComboBox(self)
            self.logic.setToolTip('Select logic')
            self.logic.addItem("=")
            self.logic.addItem("!=")
            self.logic.addItem("<")
            self.logic.addItem(">")
            self.logic.addItem("<=")
            self.logic.addItem(">=")
            self.logic.addItem("contains")
            self.logic.addItem("does not contain")
            self.buttonsWidgetLayout[self.counter + 1].addWidget(self.feature1)
            self.buttonsWidgetLayout[self.counter + 1].addWidget(self.feature2)
            self.buttonsWidgetLayout[self.counter + 1].addWidget(self.logic)
            self.buttonsWidgetLayout[self.counter + 1].addWidget(self.thresholds[self.counter + 1])
            self.vLayout.addWidget(self.buttonsWidgets[self.counter + 1])
            self.counter += 1
        else:
            pass
        

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.dialogs = list()

    # Main Window Init
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # FILTER MENU
        self.filter_menu = QtWidgets.QMenu('&Filter', self)
        self.filter_menu.addAction('&Setup', self.filterPrompt)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.filter_menu)

        # HELP MENU
        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.help_menu.addAction('&About', self.about)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        # DATA DISPLAY WIDGET
        self.table = QTableWidget(self)
        self.table.resize(100,100)
        # Our data frame goes below, current df is dummy data for testing
        self.df = pd.DataFrame({"a" : [0 ,0, 0],"b" : [0, 0, 0],"c" : [0, 0, 0]},index = [1, 2, 3])
        #df = DataFrame.read_csv("./EricTestData")
        #df = aw.data
        #df.to_csv('./EricTestData.csv')
        self.table.setColumnCount(len(self.df.columns))
        self.table.setRowCount(len(self.df.index))
        self.table.setHorizontalHeaderLabels(self.df.columns)
        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                self.table.setItem(i,j,QTableWidgetItem(str(self.df.iloc[i, j])))

        self.main_widget = QtWidgets.QWidget(self)

        self.errorLabel = QLabel('NO ERROR', self)
        
        # Canvas Setup
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.errorLabel)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.statusBar().showMessage("Testing", 2000)

    #Define All Actions Below
    
    def updateDataDisplay(self):
        #self.df = pd.DataFrame({"a" : [0 ,0, 0],"b" : [7, 8, 9],"c" : [10, 11, 12]},index = [1, 2, 3])
        #df = DataFrame.read_csv("./EricTestData")
        df = self.data
        #df.to_csv('./EricTestData.csv')
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        self.table.setHorizontalHeaderLabels(df.columns)
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.table.setItem(i, j ,QTableWidgetItem(str(df.iloc[i, j])))
        
    def filterPrompt(self):
        self.dialog = filterDialog(self)
        self.dialogs.append(self.dialog)
        self.dialog.show()

    def filterData(self):
        
        try:
            threshold = float(str(self.dialog.threshold.text()))
        except:
            threshold = str(self.dialog.threshold.text())
        f1 = str(self.dialog.feature1.currentText())
        f2 = str(self.dialog.feature2.currentText())
        logic = str(self.dialog.logic.currentText())

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", """Senior Design GUI prototype""")

if __name__ == '__main__':
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    #fd = filterDialog()
    aw.setWindowTitle("Analysis Toolkit Prototype")
    aw.show()
    sys.exit(qApp.exec_())
