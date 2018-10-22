"""
Test Module for Save and Load window
Xiangxing Liu
"""

from __future__ import unicode_literals
import sys
sys.path.insert(0, '../DBPreprocessing/')
sys.path.insert(0, '../DataAnalysis/')
import os
import csv
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


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.dialogs = list()
        self.data = pd.DataFrame({"a": [4, 5, 6], "b": [7, 8, 9], "c": [10, 11, 12]}, index=[1, 2, 3])
        self.dataUpdate = True

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
        # self.view_menu.addAction('&Data', self.dataPrompt)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.view_menu)

        # HELP MENU
        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.help_menu.addAction('&About', self.about)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        # DATA DISPLAY WIDGET
        self.table = QTableWidget(self)
        self.table.resize(100, 100)
        self.df = pd.DataFrame({"a": [4, 5, 6], "b": [7, 8, 9], "c": [10, 11, 12]}, index=[1, 2, 3])
        self.table.setColumnCount(len(self.df.columns))
        self.table.setRowCount(len(self.df.index))
        self.table.setHorizontalHeaderLabels(self.df.columns)
        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))

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

    # Define All Actions Below
    def fileOpen(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open Dataset",

                                                 "", "Baker Hughes Files (*.bh)")

        # Following block extract the last line
        tmp = ""
        with open(fileName, 'r') as f:
            for row in reversed(list(csv.reader(f))):
                tmp = ', '.join(row)
                break
        # Extract dataset
        count = 0
        XLabel = ""
        YLabel = ""
        with open(fileName, 'r') as inp, open('temp.csv', 'w') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                if not row:
                    break
                if count == 0:
                    XLabel = row[1]
                    YLabel = row[2]
                writer.writerow(row)
                count += 1

        dp = pd.read_csv('temp.csv')
        stmp = tmp.split(" ")
        tmpList = []

        # parse last line to extract coefs
        if stmp[0] == "POLY:":
            for n in stmp:
                if not n:
                    continue
                if n != "POLY:":
                    tmpList.append(float(n))
            self.coefs = [dp, tmpList]
            self.sc.update_figure(self.coefs, XLabel, YLabel, Poly=True)

        elif stmp[0] == "LINEAR:":
            count = 0
            y_int = 0.0
            s = 0.0
            rr = 0.0
            for n in stmp:
                if not n:
                    continue
                if n != "LINEAR:":
                    if count == 1:
                        y_int = float(n)
                    elif count == 2:
                        s = float(n)
                    elif count == 3:
                        rr= float(n)
                    elif count == 4:
                        self.dialog.yIntercept.isChecked = (n == "True")
                    elif count == 5:
                        self.dialog.slopeCheck.isChecked = (n == "True")
                    elif count == 6:
                        self.dialog.rSquared.isChecked = (n == "True")
                count += 1
            self.coefs = [dp, y_int, s, rr]
            self.sc.update_figure(self.coefs, XLabel, YLabel, Linear=True,
                                yint = self.dialog.yIntercept.isChecked(),
                                slope = self.dialog.slopeCheck.isChecked(),
                                rsquare = self.dialog.rSquared.isChecked())



    # Temporary Method, would be merged later
    def fileLoad(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Load File",
                                                  "", "BH Files (*.bh)")
        loadFile = pd.read_csv(fileName)

    # Temporary Method, would be merged later
    def fileExport(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Export File",
                                                  "", "CSV Files (*.csv)")
        if(self.dataUpdate):
            self.data.to_csv(fileName)
        else:
            print("Error: self.data has not been initialized")

    def fileSave(self):
        if self.data is None:
            return  # return error code bc no data to save
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save File",
                                                  "", "CSV Files (*.bh)")
        if (self.dataUpdate):
            if(self.mode_linear):
                output = pd.DataFrame({"data": self.data, "slope": self.coefs[1], "yint": self.coefs[2]},
                                      index=[0, 1, 2])
            if(self.mode_poly):
                output = pd.DataFrame({"data": self.data, "coefs": self.coefs[1][0]},
                                      index=[0, 1])
            output.to_csv(fileName)
        else:
            print("Error: self.data has not been initialized")

    def fileQuit(self):
        self.close()

    def filterPrompt(self):
        self.close()

    def filterData(self):
        self.close()

    def linearRegressionPrompt(self):
        self.close()

    def plotLinearRegression(self):
        self.close()

    def polyRegressPrompt(self):
        self.close()

    def plotPolyRegression(self):
        self.close()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", """Senior Design GUI prototype""")


if __name__ == '__main__':
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("Analysis Toolkit Prototype")
    aw.show()
    sys.exit(qApp.exec_())
