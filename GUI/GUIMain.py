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
from Init import Init
from DatabasePreprocessing import getDescriptions
import DataAnalysisModule as da

matplotlib.use('Qt5Agg')

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        #self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)
        self.axes.set_xlabel(xlabel="XXX")
        self.axes.set_ylabel(ylabel="YYY")

    def update_figure(self, data, Xlabel, Ylabel):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        # l = random.randint(0, 10)
        # dataX = dataX * l
        # dataY = dataY * l

        slope = data[1]
        yint = data[2]

        X = np.arange(0., 5., 0.2)
        Y = slope * X + yint

        sData = data[0]
        sX = sData[Xlabel].tolist()
        sY = sData[Ylabel].tolist()
        self.axes.cla()
        self.axes.scatter(sX, sY)
        self.axes.plot(X, Y)
        self.axes.set_xlabel(xlabel=Xlabel)
        self.axes.set_ylabel(ylabel=Ylabel)
        self.draw()

class dataDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(dataDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Data'
        self.left = 500
        self.top = 100
        self.width = 400
        self.height = 800
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        # COMMENTED LINES CAN ADD FUNCTIONALITY LATER
        #self.scroll = QScrollArea(self)
        #self.layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        #self.scroll.setWidget(self.table)
        #self.layout.addWidget(self.table)  
        #self.table.move(550,50)
        self.table.resize(300,400)
        # Our data frame goes below, current df is dummy data for testing
        df = pd.DataFrame({"a" : [4 ,5, 6],"b" : [7, 8, 9],"c" : [10, 11, 12]},index = [1, 2, 3])
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.table.setItem(i,j,QTableWidgetItem(str(df.iloc[i, j])))

class linearRegressionDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(linearRegressionDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Linear Regression'
        self.left = 500
        self.top = 100
        self.width = 800
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())

        label = QLabel('Linear Regression', self)
        label.move(20,90)
        label.resize(250,50)
        self.featureX = QComboBox(self)
        self.featureX.setToolTip('Select feature for X axis')
        #featureX.completer().setCompletionMode(QWidget.QCompleter.PopupCompletion)
        self.featureX.move(150, 100)
        self.featureX.addItem("Option 1")
        self.featureX.activated.connect(aw.storeXValue)
        self.featureY = QComboBox(self)
        self.featureY.setToolTip('Select feature for Y axis')
        self.featureY.move(300, 100)
        self.featureY.activated.connect(aw.storeYValue)
        '''
        #populate combo boxes
        descriptions = getDescriptions()
        descriptions.sort()
        for d in descriptions:
            if(d != "bottom depth" and d != "top depth"): continue
            self.featureY.addItem(d)
            self.featureX.addItem(d)
        '''
        yIntercept = QCheckBox("Y-Intercept",self)
        yIntercept.move(450, 100)
        rSquared = QCheckBox("R^2",self)
        rSquared.move(550, 100)
        slopeCheck = QCheckBox("Slope",self)
        slopeCheck.move(600, 100) 
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot linear regression')
        plotButton.clicked.connect(aw.plotLinearRegression)
        # plotButton.clicked.connect(lambda: sc.update_figure("XXX", "YYY"))
        plotButton.move(700,100)
        plotButton.resize(50,50)
        

class filterDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(filterDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Filter Data'
        self.left = 500
        self.top = 100
        self.width = 800
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        self.feature1 = QComboBox(self)
        self.feature1.setToolTip('Select feature 1')
        self.feature1.move(50, 100)
        self.feature1.activated.connect(aw.storeFirstValue)
        whereLabel = QLabel('WHERE', self)
        whereLabel.move(152,90)
        whereLabel.resize(250,50)
        self.feature2 = QComboBox(self)
        self.feature2.setToolTip('Select feature 2')
        self.feature2.move(200, 100)
        self.feature2.activated.connect(aw.storeSecondValue)
        '''
        descriptions = getDescriptions()
        descriptions.sort()
        for d in descriptions:
            if(d != "bottom depth" and d != "top depth"): continue
            self.feature1.addItem(d)
            self.feature2.addItem(d)
        '''
        isLabel = QLabel('IS', self)
        isLabel.move(350,90)
        isLabel.resize(250,50)
        self.logic = QComboBox(self)
        self.logic.setToolTip('Select logic')
        self.logic.addItem("=")
        self.logic.addItem("!=")
        self.logic.addItem("<")
        self.logic.addItem(">")
        self.logic.addItem("<=")
        self.logic.addItem(">=")
        self.logic.move(400, 100)
        self.logic.resize(50,25)
        self.logic.activated.connect(aw.storeLogic)
        self.threshold = QLineEdit(self)
        self.threshold.setToolTip('Input numeric value')
        self.threshold.move(500,100)
        self.threshold.resize(100,25)
        filterButton = QPushButton('Filter', self) 
        filterButton.setToolTip('Use button to filter the feature based on the chosen logic')
        filterButton.clicked.connect(aw.filterData)
        filterButton.move(700,100)
        filterButton.resize(50,50)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        
        #self.dialog = filterDialog(self)
        self.dialogs = list()
        
    # Main Window Init
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    # Drop-down Menu Bar Setup
        # FILE MENU
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Open', self.fileOpen,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.file_menu.addAction('&Save', self.fileSave,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction('&Save As', self.fileSaveAs)
        self.file_menu.addAction('&Export', self.fileExport,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        # PLOT MENU
        self.plot_menu = QtWidgets.QMenu('&Plot', self)
        self.plot_menu.addAction('&Linear Regression', self.linearRegressionPrompt)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.plot_menu)

        # FILTER MENU
        self.filter_menu = QtWidgets.QMenu('&Filter', self)
        self.filter_menu.addAction('&Setup', self.filterPrompt)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.filter_menu)

        # VIEW MENU
        self.view_menu = QtWidgets.QMenu('&View', self)
        self.view_menu.addAction('&Data', self.dataPrompt)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.view_menu)

        # HELP MENU
        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.help_menu.addAction('&About', self.about)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.main_widget = QtWidgets.QWidget(self)

        # Canvas Setup
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.sc = MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        # Plot Button
        #pbutton = QtWidgets.QPushButton('Plot')
        #pbutton.clicked.connect(lambda: sc.update_figure(t, s, "XXX", "YYY"))
        # Toolbar Setup
        #toolBar = NavigationToolbar(sc, self)

        self.layout.addWidget(self.sc)
        #layout.addWidget(toolBar)
        #layout.addWidget(pbutton)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Testing", 2000)

    #Define All Actions Below
    def fileOpen(self):
        lrd.close()

    def fileSave(self):
        self.close()

    def fileSaveAs(self):
        self.close()

    def fileExport(self):
        self.close()

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()
        
    def storeXValue(self, index):
        self.xFeature = lrd.featureX.itemText(index)
        
    def storeYValue(self, index):
        self.yFeature = lrd.featureY.itemText(index)
        
    def storeFirstValue(self, index):
        self.oneFeature = fd.feature1.itemText(index)  
        
    def storeSecondValue(self, index):
        self.twoFeature = fd.feature2.itemText(index)
        
    def storeLogic(self, index):
        self.filterLogic = fd.logic.itemText(index)
        
    def filterPrompt(self):
        self.dialog = filterDialog(self)
        self.dialogs.append(self.dialog)
        self.dialog.show()
        
    def filterData(self):
       threshold = fd.threshold.text()
       self.dialog.close()
       self.dialogs.pop()
       print(threshold)
       #filterResult = da.filtering(self.oneFeature, self.twoFeature, self.filterLogic, threshold)
        
    def dataPrompt(self):
        self.dialog = dataDialog(self)
        self.dialogs.append(self.dialog)
        self.dialog.show()
        
        
    def linearRegressionPrompt(self):
        self.dialog = linearRegressionDialog(self)
        self.dialogs.append(self.dialog)
        self.dialog.show()

    def plotLinearRegression(self):
        print(self.xFeature)
        self.dialog.close()
        self.dialogs.pop()
        #coefs = da.linearRegression(self.xFeature, self.yFeature)
        #self.data = coefs[0]
        #self.sc.update_figure(coefs, self.xFeature, self.yFeature)
	    #close linear regression window dialog

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", """Senior Design GUI prototype""")

if __name__ == '__main__':
    serverL = "MYPC\SQLEXPRESS"
    dbNameL = "BHBackupRestore"
    UIDL = "SQLDummy"
    PWDL = "bushdid9/11"
    #Init.init(serverL, dbNameL, UIDL, PWDL)
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    lrd = linearRegressionDialog()
    fd = filterDialog()
    aw.setWindowTitle("Analysis Toolkit Prototype")
    aw.show()
    sys.exit(qApp.exec_())
