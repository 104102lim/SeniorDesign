from __future__ import unicode_literals
import csv
import os
import pandas as pd

from time import sleep

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import QCoreApplication

from Init import Init
import DataAnalysis as da
import filterdialog as fd
import progressdialog as pgd
import linearregressiondialog as lrd
import polyregressiondialog as prd
import logindialog as lid
import plottingcanvas as ptc
from DatabasePreprocessing import getDescriptions


class applicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.dialog = None
        self.data = None

        # Main Window Init
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Drop-down Menu Bar Setup
        # FILE MENU
        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Open', self.fileOpen,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_O)
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
        self.plot_menu.addAction('&Polynomial Regression', self.polyRegressPrompt)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.plot_menu)

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

        self.table.resize(100, 100)
        # Our data frame goes below, current df is dummy data for testing
        self.df = pd.DataFrame({"a": [0, 0, 0], "b": [0, 0, 0], "c": [0, 0, 0]}, index=[1, 2, 3])
        self.table.setColumnCount(len(self.df.columns))
        self.table.setRowCount(len(self.df.index))
        self.table.setHorizontalHeaderLabels(self.df.columns)
        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))

        self.main_widget = QtWidgets.QWidget(self)
        self.errorLabel = QLabel('', self)
        font = self.errorLabel.font()
        font.setPointSize(12)
        self.errorLabel.setFont(font)

        # Canvas Setup
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.sc = ptc.plottingCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.layout.addWidget(self.sc)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.errorLabel)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    # Define All Actions Below

    def updateDataDisplay(self):
        df = self.data
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        self.table.setHorizontalHeaderLabels(df.columns)
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

    def fileOpen(self):
        if self.dialog is not None:
            if self.dialog.isVisible():
                return
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open Case",
                                                  "", "Baker Hughes Files (*.bh)")
        if fileName == '':
            self.errorLabel.setText('Open Error: No file name given')
            return  # no file name given
        tmp = ""
        with open(fileName, 'r') as f:
            for row in reversed(list(csv.reader(f))):
                tmp = ', '.join(row)
                break
        # Extract dataset
        towrite = ""
        with open(fileName, 'r') as inp:
            lines = inp.readlines()
            lines = lines[:-3]
            for l in lines:
                towrite += l
        with open(fileName, 'w') as out:
            out.write(towrite)

        dp = pd.read_csv(fileName, )
        with open(fileName, 'a') as out:
            out.write("\n\n" + tmp)
        labels = dp.columns
        stmp = tmp.split(" ")
        tmpList = []

        self.mode_linear = False
        self.mode_poly = False

        # parse last line to extract coefs
        if stmp[0] == "POLY:":
            self.mode_poly = True
            for n in stmp:
                if not n:
                    continue
                if n != "POLY:":
                    tmpList.append(float(n))
            XLabel = labels[0]
            YLabel = labels[1]
            self.data = dp
            self.coefs = [dp, [tmpList]]
            self.sc.update_figure(self.coefs, XLabel, YLabel, Poly=True)
            self.updateDataDisplay()

        elif stmp[0] == "LINEAR:":
            self.mode_linear = True
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
                        rr = float(n)
                    elif count == 4:
                        self.checkyint = (n == "True")
                    elif count == 5:
                        self.checkslope = (n == "True")
                    elif count == 6:
                        self.checkrsquare = (n == "True")
                count += 1
            XLabel = labels[0]
            YLabel = labels[1]
            self.data = dp
            self.coefs = [dp, s, y_int, rr]
            self.sc.update_figure(self.coefs, XLabel, YLabel, Linear=True,
                                  yint=self.checkyint,
                                  slope=self.checkslope,
                                  rsquare=self.checkrsquare)
        else:
            self.data = dp
            self.sc.clear_figure()
        self.updateDataDisplay()

    def fileExport(self):
        if self.dialog is not None:
            if self.dialog.isVisible():
                return
        if self.data is None:
            self.errorLabel.setText('Export Error: No data to export')
            return
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Export Data and Plot",
                                                  "", "CSV/PNG Files (*.csv *.png)")
        if fileName == '':
            self.errorLabel.setText('Export Error: No file name given')
            return
        fileName, extension = os.path.splitext(fileName)
        self.data.to_csv(fileName + ".csv", index=False)
        if self.mode_linear or self.mode_poly:
            self.sc.fig.savefig(fileName + ".png")

    def fileSave(self):
        if self.dialog is not None:
            if self.dialog.isVisible():
                return
        if self.data is None:
            self.errorLabel.setText('Save Error: No data to save')
            return
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Case",
                                                  "", "Baker Hughes Files (*.bh)")
        if fileName == '':
            self.errorLabel.setText('Save Error: No file name given')
            return
        output = self.data.copy()
        output.to_csv(fileName, index=False)
        file = open(fileName, 'a')
        if self.mode_linear:
            file.write("\n\nLINEAR: " +
                       str(self.coefs[2]) + " " +
                       str(self.coefs[1][0]) + " " +
                       str(self.coefs[3]) + " " +
                       str(self.checkyint) + " " +
                       str(self.checkslope) + " " +
                       str(self.checkrsquare) + " ")
        elif self.mode_poly:
            file.write("\n\nPOLY: ")
            for c in self.coefs[1][0]:
                file.write(str(c) + " ")

        else:
            file.write("\n\nDATA: ")
        file.close()

    def fileQuit(self):
        self.close()

    def filterPrompt(self):
        if self.dialog is not None:
            if self.dialog.isVisible():
                return
        self.dialog = fd.filterDialog(self)
        self.dialog.show()

    def filterData(self):
        threshs = []
        feat1s = []
        feat2s = []
        logics = []
        numfilters = self.dialog.counter + 1
        for i in range(numfilters):
            threshs.append(self.dialog.threshold[i].text())
            feat1s.append(self.dialog.feature1[i].currentText())
            feat2s.append(self.dialog.feature2[i].currentText())
            logics.append(self.dialog.logic[i].currentText())
        for i in range(numfilters):
            try:
                threshs[i] = float(str(threshs[i]))
            except:
                threshs[i] = str(threshs[i])
            feat1s[i] = str(feat1s[i])
            feat2s[i] = str(feat2s[i])
            logics[i] = str(logics[i])
        descriptions = getDescriptions()
        for i in range(numfilters):
            if (feat2s[i] not in descriptions) \
                    or ((feat1s[i] not in descriptions) and (i == 0)):
                self.errorLabel.setText("One or more of the feature names were invalid.")
                self.dialog.close()
                self.dialog = None
                return
            if type(threshs[i]) is str:
                if threshs[i] == "":
                    self.errorLabel.setText("One or more threshold value was empty")
                    self.dialog.close()
                    self.dialog = None
                    return
        try:
            filterResult = da.filtering(feat1s[0], feat2s, logics, threshs,
                                    [feat1s[i] for i in range(1, numfilters)])
        except:
            self.errorLabel.setText("An error occurred while loading or analyzing the data.")
            self.dialog.close()
            self.dialog = None
        if type(filterResult) == str:
            self.errorLabel.setText(filterResult)
            self.dialog.close()
            self.dialog = None
        else:
            self.mode_linear = False
            self.mode_poly = False
            self.sc.clear_figure()
            self.errorLabel.setText("")
            self.data = filterResult[1]
            self.updateDataDisplay()
            self.dialog.close()
            self.dialog = None

    def linearRegressionPrompt(self):
        if self.dialog is not None:
            if self.dialog.isVisible():
                return
        self.dialog = lrd.linearRegressionDialog(self)
        self.dialog.show()

    def plotLinearRegression(self):
        x = str(self.dialog.featureX.currentText())
        y = str(self.dialog.featureY.currentText())
        descriptions = getDescriptions()
        if (x not in descriptions) or (y not in descriptions):
            self.errorLabel.setText("One or more feature names were invalid")
            self.dialog.close()
            self.dialog = None
            return
        try:
            self.coefs = da.linearRegression(x, y)
        except:
            self.errorLabel.setText("An error occurred while loading or analyzing the data.")
            self.dialog.close()
            self.dialog = None
        self.checkyint = self.dialog.yIntercept.isChecked()
        self.checkslope = self.dialog.slopeCheck.isChecked()
        self.checkrsquare = self.dialog.rSquared.isChecked()
        if (type(self.coefs) == str):
            self.errorLabel.setText(self.coefs)
            self.dialog.close()
            self.dialog = None
        else:
            self.mode_linear = True
            self.mode_poly = False
            self.data = self.coefs[0]
            self.errorLabel.setText("")
            self.sc.update_figure(self.coefs, x, y, Linear=True,
                                  yint=self.dialog.yIntercept.isChecked(),
                                  slope=self.dialog.slopeCheck.isChecked(),
                                  rsquare=self.dialog.rSquared.isChecked())
            self.updateDataDisplay()
            self.dialog.close()
            self.dialog = None

    def polyRegressPrompt(self):
        if self.dialog is not None:
            if self.dialog.isVisible():
                return
        self.dialog = prd.polyRegressionDialog(self)
        self.dialog.show()

    def plotPolyRegression(self):
        x = str(self.dialog.featureX.currentText())
        y = str(self.dialog.featureY.currentText())
        order = int(self.dialog.order.currentText())
        descriptions = getDescriptions()
        if (x not in descriptions) or (y not in descriptions):
            self.errorLabel.setText("One or more feature names were invalid")
            self.dialog.close()
            self.dialog = None
            return
        try:
            self.coefs = da.polynomialRegression(x, y, order)
        except:
            self.errorLabel.setText("An error occurred while loading or analyzing the data.")
            self.dialog.close()
            self.dialog = None
        if (type(self.coefs) == str):
            self.errorLabel.setText(self.coefs)
            self.dialog.close()
            self.dialog = None
        else:
            self.mode_linear = False
            self.mode_poly = True
            self.data = self.coefs[0]
            self.errorLabel.setText("")
            self.sc.update_figure(self.coefs, x, y, Poly=True)
            self.updateDataDisplay()
            self.dialog.close()
            self.dialog = None

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", "The Baker Hughes Data Analysis Toolkit " +
                                    "was developed by University of Texas students Paul Heath, " +
                                    "Sungho Lim, Eric Ramos, Xianxing Liu, and Guiseppe Gallardo.\n\nThis " +
                                    "application allows the user to run linear and polynomial regression on " +
                                    "selected datasets. Linear regression contains the options to compute the " +
                                    "Y-intercept, R^2, and slope of the selected data. Polynomial regression " +
                                    "allows the user the option to increase or decrease the order of the " +
                                    "analysis equation to obtain the best fit of the selected data. Users " +
                                    "can filter data by applying constraints to datasets for closer inspection. " +
                                    "Assorted file management methods are included for the benefit of the user. " +
                                    "\n\nThis application uses libraries licensed under the GNU GPL. Consider " +
                                    "this before any commercial production or distribution.")

    def loginPrompt(self):
        if self.dialog is not None:
            if self.dialog.isVisible():
                return
        self.dialog = lid.loginDialog(self)
        self.dialog.show()

    def login(self):
        machine = str(self.dialog.server.text())
        portLog = str(self.dialog.port.text())
        database = str(self.dialog.databaseName.text())
        userName = str(self.dialog.username.text())
        passWord = str(self.dialog.password.text())
        self.dialog.close()
        self.dialog = None

        self.dialog = pgd.progressDialog(self)
        self.dialog.show()
        QCoreApplication.processEvents()
        ret = Init.connect(machine, portLog, database, userName, passWord)
        if ret is not None:
            self.dialog.updateConnectFail()
            QCoreApplication.processEvents()
            sleep(4)
            self.dialog.close()
            self.dialog = None
            self.loginPrompt()
        else:
            self.dialog.updateConnect()
            QCoreApplication.processEvents()
            Init.gettableinfo()
            self.dialog.updateTable()
            QCoreApplication.processEvents()
            Init.maketrees()
            self.dialog.updateTree()
            QCoreApplication.processEvents()
            sleep(2)
            self.dialog.close()
            self.dialog = None
            self.show()
