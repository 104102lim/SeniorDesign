from __future__ import unicode_literals
import csv
import sys
import os
import matplotlib
import numpy as np
import pandas as pd

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QPushButton, QCheckBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog, QProgressBar
from PyQt5.QtCore import QBasicTimer, Qt

from Init import Init
from DatabasePreprocessing import getDescriptions
import DataAnalysis as da
import filterdialog as fd

matplotlib.use('Qt5Agg')

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def clear_figure(self):
        self.axes.cla()
        self.draw()

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
        # attempt at completion
        # try:
        #     comp = QCompleter(descriptions.copy())
        #     comp.setCompletionMode(QCompleter.PopupCompletion)
        #     self.featureX.setCompleter(comp)
        #     self.featureX.setEditable(True)
        # except Exception as e:
        #     print(e)
        for d in descriptions:
            if(d != "bottom depth"
                    and d != "top depth"
                    and d != "Cost per unit"
                    and d != "Name of mud engineer"):
                continue
            self.featureY.addItem(d)
            self.featureX.addItem(d)
        self.yIntercept = QCheckBox("Y-Intercept", self)
        self.yIntercept.move(450, 100)
        self.rSquared = QCheckBox("R^2", self)
        self.rSquared.move(550, 100)
        self.slopeCheck = QCheckBox("Slope", self)
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
        descriptions = getDescriptions()
        descriptions = [d.lower() for d in descriptions]
        descriptions.sort()
        self.featureX.setInsertPolicy(QComboBox.NoInsert)
        self.featureX.setEditable(True)
        self.featureX.setCompleter(QCompleter(descriptions))
        self.featureX.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.featureY.setInsertPolicy(QComboBox.NoInsert)
        self.featureY.setEditable(True)
        self.featureY.setCompleter(QCompleter(descriptions))
        self.featureY.completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.order = QComboBox(self)
        self.order.setToolTip('Select order of polynomial fit')
        self.order.move(450, 100)
        for i in range(1, 10):
            self.order.addItem(str(i))
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot poly regression')
        plotButton.clicked.connect(aw.plotPolyRegression)
        plotButton.move(700,100)
        plotButton.resize(50,50)
        
class loginDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(loginDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'User Login'
        self.left = 200
        self.top = 100
        self.width = 450
        self.height = 370
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
        
        
        # input boxes and labels
        label = QLabel('Machine Name/IP', self)
        label.move(80, 60)
        label.resize(150, 30)
        self.server = QLineEdit(self)
        self.server.setToolTip('Enter Machine Name/IP')
        self.server.move(200, 60)
        self.server.resize(130, 30)
        label = QLabel('Port/Instance', self)
        label.move(80, 100)
        label.resize(150, 30)
        self.port = QLineEdit(self)
        self.port.setToolTip('Enter Port/Instance')
        self.port.move(200, 100)
        self.port.resize(130, 30)
        label = QLabel('Database Name', self)
        label.move(80, 140)
        label.resize(150, 30)
        self.databaseName = QLineEdit(self)
        self.databaseName.setToolTip('Enter Database Name')
        self.databaseName.move(200, 140)
        self.databaseName.resize(130, 30)
        label = QLabel('Username', self)
        label.move(80, 180)
        label.resize(150, 30)
        self.username = QLineEdit(self)
        self.username.setToolTip('Enter Username')
        self.username.move(200, 180)
        self.username.resize(130, 30)
        label = QLabel('Password', self)
        label.move(80, 220)
        label.resize(150, 30)
        self.password = QLineEdit(self)
        self.password.setToolTip('Enter Password')
        self.password.move(200, 220)
        self.password.resize(130, 30)
        enterButton = QPushButton('Login', self)
        enterButton.setToolTip('Login')
        enterButton.clicked.connect(aw.login)
        enterButton.move(224, 260)
        enterButton.resize(80, 50)


class ProgressBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('ProgressBar')
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        # self.button = QPushButton('Start', self)
        # self.button.setFocusPolicy(Qt.NoFocus)
        # self.button.move(40, 80)
        #
        # self.button.clicked.connect(self.onStart)
        self.timer = QBasicTimer()
        self.step = 0

        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)


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
        df = self.data
        #df.to_csv('./EricTestData.csv')
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df.index))
        self.table.setHorizontalHeaderLabels(df.columns)
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.table.setItem(i, j ,QTableWidgetItem(str(df.iloc[i, j])))
        
        
    def fileOpen(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                        "Open Case",
                        "", "Baker Hughes Files (*.bh)")
        if fileName == '':
            return #no file name given
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
        if self.data is None:
            return  # return error code bc no data to save
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Export Data and Plot",
                                                  "", "CSV/PNG Files (*.csv *.png)")
        if fileName == '':
            return #no file name given
        fileName, extension = os.path.splitext(fileName)
        self.data.to_csv(fileName + ".csv", index=False)
        if self.mode_linear or self.mode_poly:
            self.sc.fig.savefig(fileName + ".png")

    def fileSave(self):
        if self.data is None:
            return  # return error code bc no data to save
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save Case",
                                                  "", "Baker Hughes Files (*.bh)")
        if fileName == '':
            return #no file name given
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
            return
        self.dialog = fd.filterDialog(self)
        self.dialog.show()

    def filterData(self):
        self.mode_linear = False
        self.mode_poly = False
        self.sc.clear_figure()
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
        filterResult = da.filtering(feat1s[0], feat2s, logics, threshs,
                                    [feat1s[i] for i in range(1, numfilters)])
        if (type(filterResult) == str):
            self.errorLabel.setText(filterResult)
            self.dialog.close()
            self.dialog = None

        else:
            self.errorLabel.setText("")
            self.data = filterResult[1]
            self.updateDataDisplay()
            self.dialog.close()
            self.dialog = None


    def linearRegressionPrompt(self):
        if self.dialog is not None:
            return
        self.dialog = linearRegressionDialog(self)
        self.dialog.show()

    def plotLinearRegression(self):
        self.mode_linear = True
        self.mode_poly = False
        x = str(self.dialog.featureX.currentText())
        y = str(self.dialog.featureY.currentText())
        self.coefs = da.linearRegression(x, y)
        self.checkyint = self.dialog.yIntercept.isChecked()
        self.checkslope = self.dialog.slopeCheck.isChecked()
        self.checkrsquare = self.dialog.rSquared.isChecked()
        if (type(self.coefs) == str):
            self.errorLabel.setText(self.coefs)
        self.coefs = da.linearRegression(x, y)
        if (type(self.coefs) == str):
            self.errorLabel.setText(self.coefs)
            self.dialog.close()
            self.dialog = None
           
        else:
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
            return
        self.dialog = polyRegressionDialog(self)
        self.dialog.show()

    def plotPolyRegression(self):
        self.mode_linear = False
        self.mode_poly = True
        x = str(self.dialog.featureX.currentText())
        y = str(self.dialog.featureY.currentText())
        order = int(self.dialog.order.currentText())
        self.coefs = da.polynomialRegression(x, y, order)
        if (type(self.coefs) == str):
            self.errorLabel.setText(self.coefs)
            self.dialog.close()
            self.dialog = None
        else:
            self.data = self.coefs[0]
            self.errorLabel.setText("")
            self.sc.update_figure(self.coefs, x, y, Poly=True)
            self.updateDataDisplay()
            self.dialog.close()
            self.dialog = None

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", """Senior Design GUI prototype""")

    def loginPrompt(self):
        if self.dialog is not None:
            return
        self.dialog = loginDialog(self)
        self.dialog.show()

    def login(self):
        machine = str(self.dialog.server.text())
        portLog = str(self.dialog.port.text())
        database = str(self.dialog.databaseName.text())
        userName = str(self.dialog.username.text())
        passWord = str(self.dialog.password.text())
        if(True):
            machine = "MSI\SQLEXPRESS"
            portLog = ""
            database = "senior_design"
            userName = "SQLBH"
            passWord = "mudtable"
            '''
            machine = "MYPC\SQLEXPRESS"
            portLog = ""
            database = "BHBackupRestore"
            userName = "SQLDummy"
            passWord = "bushdid9/11"
            '''
        self.dialog.close()
        self.dialog = None
        self.dialog = ProgressBar(self);
        self.dialog.show()
        Init.init(machine, portLog, database, userName, passWord)
        self.dialog.close()
        self.dialog = None
        self.show()

if __name__ == '__main__':
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("Analysis Toolkit Prototype")
    aw.loginPrompt()
    sys.exit(qApp.exec_())
