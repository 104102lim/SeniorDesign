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

        if(Linear):
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

        if(Poly):
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
        self.featureY = QComboBox(self)
        self.featureY.setToolTip('Select feature for Y axis')
        self.featureY.move(300, 100)
        #populate combo boxes
        descriptions = getDescriptions()
        descriptions.sort()
        for d in descriptions:
            if(d != "bottom depth" and d != "top depth" and d != "Cost per unit"): continue
            self.featureY.addItem(d)
            self.featureX.addItem(d)
        self.yIntercept = QCheckBox("Y-Intercept",self)
        self.yIntercept.move(450, 100)
        self.rSquared = QCheckBox("R^2",self)
        self.rSquared.move(550, 100)
        self.slopeCheck = QCheckBox("Slope",self)
        self.slopeCheck.move(600, 100) 
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot linear regression')
        plotButton.clicked.connect(aw.plotLinearRegression)
        plotButton.move(700,100)
        plotButton.resize(50,50)


class polyRegressionDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(polyRegressionDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Poly Regression'
        self.left = 500
        self.top = 100
        self.width = 800
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())

        label = QLabel('Poly Regression', self)
        label.move(20,90)
        label.resize(250,50)
        self.featureX = QComboBox(self)
        self.featureX.setToolTip('Select feature for X axis')
        self.featureX.move(150, 100)
        self.featureY = QComboBox(self)
        self.featureY.setToolTip('Select feature for Y axis')
        self.featureY.move(300, 100)
        self.order = QComboBox(self)
        self.order.setToolTip('Select order of polynomial fit')
        self.order.move(450, 100)
        for i in range(1, 10):
            self.order.addItem(str(i))
        descriptions = getDescriptions()
        descriptions.sort()
        for d in descriptions:
            if(d != "bottom depth" and d != "top depth" and d != "Cost per unit"): continue
            self.featureY.addItem(d)
            self.featureX.addItem(d)
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot poly regression')
        plotButton.clicked.connect(aw.plotPolyRegression)
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
        whereLabel = QLabel('WHERE', self)
        whereLabel.move(152,90)
        whereLabel.resize(250,50)
        self.feature2 = QComboBox(self)
        self.feature2.setToolTip('Select feature 2')
        self.feature2.move(200, 100)
        descriptions = getDescriptions()
        descriptions.sort()
        for d in descriptions:
            if(d != "bottom depth" and d != "top depth" and d != "Cost per unit"): continue
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
        self.logic.addItem("contains")
        self.logic.addItem("does not contain")
        self.logic.move(400, 100)
        self.logic.resize(50,25)
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
        self.dialogs = list()

    # Main Window Init
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    # Drop-down Menu Bar Setup
        # FILE MENU
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Open', self.fileOpen,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_O)
        self.file_menu.addAction('&Load', self.fileLoad,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_L)
        self.file_menu.addAction('&Export', self.fileExport,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_E)
        self.file_menu.addAction('&Save', self.fileSave,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        # PLOT MENU
        self.plot_menu = QtWidgets.QMenu('&Plot', self)
        self.plot_menu.addAction('&Linear Regression', self.linearRegressionPrompt)
        self.plot_menu.addAction('&Poly Regression', self.polyRegressPrompt)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.plot_menu)

        # FILTER MENU
        self.filter_menu = QtWidgets.QMenu('&Filter', self)
        self.filter_menu.addAction('&Setup', self.filterPrompt)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.filter_menu)

        # VIEW MENU
        self.view_menu = QtWidgets.QMenu('&View', self)
        #self.view_menu.addAction('&Data', self.dataPrompt)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.view_menu)

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
        self.sc = MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.layout.addWidget(self.sc)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.errorLabel)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.statusBar().showMessage("Testing", 2000)

    #Define All Actions Below
    
    def updateDataDisplay(self):
        #self.df = pd.DataFrame({"a" : [0 ,0, 0],"b" : [7, 8, 9],"c" : [10, 11, 12]},index = [1, 2, 3])
        #df = DataFrame.read_csv("./EricTestData")
        df = aw.data
        #df.to_csv('./EricTestData.csv')
        self.table.setColumnCount(len(self.df.columns))
        self.table.setRowCount(len(self.df.index))
        self.table.setHorizontalHeaderLabels(self.df.columns)
        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                self.table.setItem(i,j,QTableWidgetItem(str(self.df.iloc[i, j])))
        
        
    def fileOpen(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                        "Open Dataset",
                        "", "CSV Files (*.csv)")

    # Temporary Method, would be merged later
    def fileLoad(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                        "Load File",
                        "", "BH Files (*.bh)")

    # Temporary Method, would be merged later
    def fileExport(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                        "Export File",
                        "", "BH Files (*.bh)")

    def fileSave(self):
        if self.data is None:
           return #return error code bc no data to save
        fileName, _ = QFileDialog.getSaveFileName(self,
                        "Save Dataset",
                        "", "CSV Files (*.csv)")

    def fileQuit(self):
        self.close()

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
        filterResult = da.filtering(f1, f2, logic, threshold)
        if (type(filterResult) == str):
            self.errorLabel.setText(filterResult)
        else:
            self.data = filterResult[1]
            self.updateDataDisplay()
            self.dialog.close()
            self.dialogs.pop()

    def linearRegressionPrompt(self):
        self.dialog = linearRegressionDialog(self)
        self.dialogs.append(self.dialog)
        self.dialog.show()

    def plotLinearRegression(self):
        x = str(self.dialog.featureX.currentText())
        y = str(self.dialog.featureY.currentText())
        coefs = da.linearRegression(x, y)
        if (type(coefs) == str):
            self.errorLabel.setText(coefs)
        else:
            self.data = coefs[0]
            self.sc.update_figure(coefs, x, y, Linear=True,
                              yint=self.dialog.yIntercept.isChecked(),
                              slope=self.dialog.slopeCheck.isChecked(),
                              rsquare=self.dialog.rSquared.isChecked())
            self.updateDataDisplay()
            self.dialog.close()
            self.dialogs.pop()

    def polyRegressPrompt(self):
        self.dialog = polyRegressionDialog(self)
        self.dialogs.append(self.dialog)
        self.dialog.show()

    def plotPolyRegression(self):
        x = str(self.dialog.featureX.currentText())
        y = str(self.dialog.featureY.currentText())
        order = int(self.dialog.order.currentText())
        coefs = da.polynomialRegression(x, y, order)
        if (type(coefs) == str):
            self.errorLabel.setText(coefs)
        else:
            self.data = coefs[0]
            self.sc.update_figure(coefs, x, y, Poly=True)
            self.updateDataDisplay()
            self.dialog.close()
            self.dialogs.pop()

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
    aw.setWindowTitle("Analysis Toolkit Prototype")
    aw.show()
    sys.exit(qApp.exec_())
