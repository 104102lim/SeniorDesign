#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 13:50:26 2018

@author: JoeyGallardo
"""
from __future__ import unicode_literals
import sys
sys.path.insert(0, '../DBPreprocessing/')
sys.path.insert(0, '../DataAnalysis/')
import os
import random
import matplotlib
import numpy as np
import pandas as pd
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QPushButton,QCheckBox
from PyQt5.QtWidgets import QScrollArea, QTableWidget,QVBoxLayout, QTableWidgetItem, QWidget
from PyQt5.QtWidgets import QFileDialog

"""class errorLogin(QtWidgets.QMainWindow):
     def __init__(self):
        self.dialogs = list()

    # Main Window Init
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Login Error'
        self.left = 200
        self.top = 100
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        #input boxes and labels
        label = QLabel('Invalid Credentials. Please Try Again.', self)
        label.move(30,50)
        label.resize(400,80)
        retryButton = QPushButton('Login', self) 
        retryButton.setToolTip('Login')
        retryButton.clicked.connect(aw.loginWindowDialog)
        retryButton.move(224,260)
        retryButton.resize(80,50)
"""
class loginWindowDialog(QtWidgets.QMainWindow):
    def __init__(self):
        self.dialogs = list()

    # Main Window Init
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'User Login'
        self.left = 200
        self.top = 100
        self.width = 450
        self.height = 370
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        #input boxes and labels
        label = QLabel('Machine Name/IP', self)
        label.move(80,60)
        label.resize(150,30)
        self.server = QLineEdit(self)
        self.server.setToolTip('Enter Machine Name/IP')
        self.server.move(200,60)
        self.server.resize(130,30)
        label = QLabel('Port/Instance', self)
        label.move(80,100)
        label.resize(150,30)
        self.port = QLineEdit(self)
        self.port.setToolTip('Enter Port/Instance')
        self.port.move(200,100)
        self.port.resize(130,30)
        label = QLabel('Database Name', self)
        label.move(80,140)
        label.resize(150, 30)
        self.databaseName = QLineEdit(self)
        self.databaseName.setToolTip('Enter Database Name')
        self.databaseName.move(200,140)
        self.databaseName.resize(130,30)
        label = QLabel('Username', self)
        label.move(80,180)
        label.resize(150,30)
        self.username = QLineEdit(self)
        self.username.setToolTip('Enter Username')
        self.username.move(200,180)
        self.username.resize(130,30)
        label = QLabel('Password', self)
        label.move(80,220)
        label.resize(150, 30)
        self.password = QLineEdit(self)
        self.password.setToolTip('Enter Password')
        self.password.move(200,220)
        self.password.resize(130,30)
        enterButton = QPushButton('Login', self) 
        enterButton.setToolTip('Login')
        enterButton.clicked.connect(self.checkLogin)
        enterButton.move(224,260)
        enterButton.resize(80,50)
 
    def checkLogin(self):
        machine = str(self.server.text())
        portLog = str(self.port.text())
        database = str(self.databaseName.text())
        userName = str(self.username.text())
        passWord = str(self.password.text())
        #Init.init(machine, database, userName, passWord)
        #aw.show()
            
            
            
            
        
    
if __name__ == '__main__':
    serverL = "MYPC\SQLEXPRESS"
    realPort = "Paul"
    dbNameL = "BHBackupRestore"
    UIDL = "SQLDummy"
    PWDL = "bushdid9/11"
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    aw = loginWindowDialog()
    aw.setWindowTitle("Baker Hughes Oil Based Characterization")
    aw.show()
    sys.exit(qApp.exec_())