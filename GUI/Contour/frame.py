# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------
    frame.py
    
    GUI Module
    
    @author: Eric Ramos
---------------------------------------------------------------
"""

import sys
import pandas as pd
from PyQt5.QtWidgets import QComboBox, QLineEdit, QMainWindow, QLabel, QApplication, QPushButton,QCheckBox
from PyQt5.QtWidgets import QScrollArea, QTableWidget,QVBoxLayout, QTableWidgetItem, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QMainWindow):
 
    def __init__(self):
        #super().__init__()
        super(App, self).__init__()
        self.title = 'Analysis Toolkit Prototype'
        self.left = 500
        self.top = 100
        self.width = 800
        self.height = 800
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
####### LINEAR REGRESSION #######
        label = QLabel('Linear Regression', self)
        label.move(20,490)
        label.resize(250,50)
        featureX = QComboBox(self)
        featureX.setToolTip('Select feature for X axis')
        featureX.addItem("Option 1")
        featureX.addItem("Option 2")
        featureX.move(150, 500)
        featureY = QComboBox(self)
        featureY.setToolTip('Select feature for Y axis')
        featureY.addItem("Option 1")
        featureY.addItem("Option 2")
        featureY.move(300, 500)
        yIntercept = QCheckBox("Y-Intercept",self)
        yIntercept.move(450, 500)
        rSquared = QCheckBox("R^2",self)
        rSquared.move(550, 500)
        slopeCheck = QCheckBox("Slope",self)
        slopeCheck.move(600, 500) 
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot linear regression')
        plotButton.clicked.connect(self.on_click)
        plotButton.move(700,500)
        plotButton.resize(50,50)
        
####### FILTERING #######
        feature1 = QComboBox(self)
        feature1.setToolTip('Select feature 1')
        feature1.addItem("Option 1")
        feature1.addItem("Option 2")
        feature1.move(50, 600)
        whereLabel = QLabel('WHERE', self)
        whereLabel.move(152,590)
        whereLabel.resize(250,50)
        feature2 = QComboBox(self)
        feature2.setToolTip('Select feature 2')
        feature2.addItem("Option 1")
        feature2.addItem("Option 2")
        feature2.move(200, 600)
        isLabel = QLabel('IS', self)
        isLabel.move(350,590)
        isLabel.resize(250,50)
        logic = QComboBox(self)
        logic.setToolTip('Select logic')
        logic.addItem("<")
        logic.addItem(">")
        logic.move(400, 600)
        logic.resize(50,25)
        self.threshold = QLineEdit(self)
        self.threshold.setToolTip('Input numeric value')
        self.threshold.move(500,600)
        self.threshold.resize(100,25)
        filterButton = QPushButton('Filter', self) 
        filterButton.setToolTip('Use button to filter the feature based on the chosen logic')
        filterButton.clicked.connect(self.display_input)
        filterButton.move(700,600)
        filterButton.resize(50,50)
        
####### RAW OUTPUT DATA SAMPLE #######
        #self.scroll = QScrollArea(self)
        #self.layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        #self.scroll.setWidget(self.table)
        #self.layout.addWidget(self.table)  
        self.table.move(550,50)
        self.table.resize(200,400)
        df = pd.DataFrame({"a" : [4 ,5, 6],"b" : [7, 8, 9],"c" : [10, 11, 12]},index = [1, 2, 3])
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.table.setItem(i,j,QTableWidgetItem(str(df.iloc[i, j])))
                
####### FILE OPTIONS ####### 
        saveButton = QPushButton('Save', self) 
        saveButton.setToolTip('Use button to save the query')
        #saveButton.clicked.connect(self.save)
        saveButton.move(250,700)
        saveButton.resize(100,50)
        loadButton = QPushButton('Load', self) 
        loadButton.setToolTip('Use button to load a query')
        #loadButton.clicked.connect(self.load)
        loadButton.move(350,700)
        loadButton.resize(100,50)
        exportButton = QPushButton('Export', self) 
        exportButton.setToolTip('Use button to export a query')
        #exportButton.clicked.connect(self.export)
        exportButton.move(450,700)
        exportButton.resize(100,50)

### ACTION METHODS ###
    @pyqtSlot()    
    def on_click(self):
        print('Plot graph')
        label2 = QLabel('Linear Regression', self)
        label2.move(20,100)
    def display_input(self):
        textboxValue = self.threshold.text();
        print("You typed" + " " + textboxValue)
        
if __name__ == '__main__':
    app = 0
    app = QApplication(sys.argv)
    main = App()
    main.show()
    #main.showMaximized()
    sys.exit(app.exec_())