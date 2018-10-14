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
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_figure(self, data, Xlabel, Ylabel, yint, slope, rsquare):
        # Tasks to do:
        # change color
        # add legend for R2, yint, slope
        # Add title
        # Extend line

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

        slope_hat = data[1]
        yint_hat = data[2]
        X = np.arange(xmin, xmax, interval)
        Y = slope_hat * X + yint_hat

        self.axes.cla()
        self.axes.scatter(sX, sY, color='green')
        self.axes.plot(X, Y, color='red')
        self.axes.set_xlabel(xlabel=Xlabel)
        self.axes.set_ylabel(ylabel=Ylabel)
        self.axes.set_title("Linear Regression: " + Ylabel + " vs. " + Xlabel)
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
        #df = pd.DataFrame({"a" : [4 ,5, 6],"b" : [7, 8, 9],"c" : [10, 11, 12]},index = [1, 2, 3])
        #df = DataFrame.read_csv("./EricTestData")
        df = aw.data
        #df.to_csv('./EricTestData.csv')
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        self.table.setHorizontalHeaderLabels(df.columns)
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
        self.featureX.move(150, 100)
        self.featureX.activated.connect(aw.storeXValue)
        self.featureY = QComboBox(self)
        self.featureY.setToolTip('Select feature for Y axis')
        self.featureY.move(300, 100)
        self.featureY.activated.connect(aw.storeYValue)
        #populate combo boxes
        descriptions = getDescriptions()
        descriptions.sort()
        for d in descriptions:
            if(d != "bottom depth" and d != "top depth"): continue
            self.featureY.addItem(d)
            self.featureX.addItem(d)
        self.yIntercept = QCheckBox("Y-Intercept",self)
        self.yIntercept.move(450, 100)
        self.yIntercept.stateChanged.connect(aw.clickYIntercept)
        self.rSquared = QCheckBox("R^2",self)
        self.rSquared.move(550, 100)
        self.rSquared.stateChanged.connect(aw.clickRSquared)
        self.slopeCheck = QCheckBox("Slope",self)
        self.slopeCheck.move(600, 100) 
        self.slopeCheck.stateChanged.connect(aw.clickSlope)
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot linear regression')
        plotButton.clicked.connect(aw.plotLinearRegression)
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
        descriptions = getDescriptions()
        descriptions.sort()
        for d in descriptions:
            if(d != "bottom depth" and d != "top depth"): continue
            self.feature1.addItem(d)
            self.feature2.addItem(d)
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

    def getThreshold(self):
        return self.threshold.text()

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
        self.layout.addWidget(self.sc)
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
       threshold = float(self.dialog.getThreshold())
       filterResult = da.filtering(self.oneFeature, self.twoFeature, self.filterLogic, threshold)
       self.data = filterResult[1]
       self.dialog.close()
       self.dialogs.pop()

    def dataPrompt(self):
        self.dialog = dataDialog(self)
        self.dialogs.append(self.dialog)
        self.dialog.show()

    def linearRegressionPrompt(self):
        self.dialog = linearRegressionDialog(self)
        self.dialogs.append(self.dialog)
        self.dialog.show()

    def plotLinearRegression(self):
        coefs = da.linearRegression(self.xFeature, self.yFeature)
        self.data = coefs[0]
        self.sc.update_figure(coefs, self.xFeature, self.yFeature, self.yChecked, self.sChecked, self.rChecked)
        self.dialog.close()
        self.dialogs.pop()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", """Senior Design GUI prototype""")
        
    def clickYIntercept(self,state):
        if state == QtCore.Qt.Checked:
            self.yChecked = True
        else:
            self.yChecked = False
            
    def clickRSquared(self,state):
        if state == QtCore.Qt.Checked:
            self.rChecked = True
        else:
            self.rChecked = False
            
    def clickSlope(self,state):
        if state == QtCore.Qt.Checked:
            self.sChecked = True
        else:
            self.sChecked = False

if __name__ == '__main__':
    serverL = "MYPC\SQLEXPRESS"
    dbNameL = "BHBackupRestore"
    UIDL = "SQLDummy"
    PWDL = "bushdid9/11"
    Init.init(serverL, dbNameL, UIDL, PWDL)
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    lrd = linearRegressionDialog()
    fd = filterDialog()
    aw.setWindowTitle("Analysis Toolkit Prototype")
    aw.show()
    sys.exit(qApp.exec_())
