# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------
frame_test
---------------------------------------------------------------
"""

from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
# Uncomment this line before running, it breaks sphinx-gallery builds
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QLabel, QPushButton,QCheckBox

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """
    Canvas Module
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

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

    def update_figure(self, dataX, dataY, Xlabel, Ylabel):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = random.randint(0, 10)

        dataX = dataX * l
        dataY = dataY * l

        self.axes.cla()
        self.axes.plot(dataX, dataY)
        self.axes.set_xlabel(xlabel=Xlabel)
        self.axes.set_ylabel(ylabel=Ylabel)
        self.draw()

class linearRegressionDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(linearRegressionDialog, self).__init__(parent)
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
        featureX = QComboBox(self)
        featureX.setToolTip('Select feature for X axis')
        featureX.addItem("Option 1")
        featureX.addItem("Option 2")
        #featureX.completer().setCompletionMode(QWidget.QCompleter.PopupCompletion)
        featureX.move(150, 100)
        featureY = QComboBox(self)
        featureY.setToolTip('Select feature for Y axis')
        featureY.addItem("Option 1")
        featureY.addItem("Option 2")
        featureY.move(300, 100)
        yIntercept = QCheckBox("Y-Intercept",self)
        yIntercept.move(450, 100)
        rSquared = QCheckBox("R^2",self)
        rSquared.move(550, 100)
        slopeCheck = QCheckBox("Slope",self)
        slopeCheck.move(600, 100) 
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot linear regression')
        #plotButton.clicked.connect(self.on_click)
        plotButton.move(700,100)
        plotButton.resize(50,50)

class filterDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(filterDialog, self).__init__(parent)
        self.title = 'Filter Data'
        self.left = 500
        self.top = 100
        self.width = 800
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        
        feature1 = QComboBox(self)
        feature1.setToolTip('Select feature 1')
        feature1.addItem("Option 1")
        feature1.addItem("Option 2")
        feature1.move(50, 100)
        whereLabel = QLabel('WHERE', self)
        whereLabel.move(152,90)
        whereLabel.resize(250,50)
        feature2 = QComboBox(self)
        feature2.setToolTip('Select feature 2')
        feature2.addItem("Option 1")
        feature2.addItem("Option 2")
        feature2.move(200, 100)
        isLabel = QLabel('IS', self)
        isLabel.move(350,90)
        isLabel.resize(250,50)
        logic = QComboBox(self)
        logic.setToolTip('Select logic')
        logic.addItem("=")
        logic.addItem("!=")
        logic.addItem("<")
        logic.addItem(">")
        logic.addItem("<=")
        logic.addItem(">=")
        logic.move(400, 100)
        logic.resize(50,25)
        self.threshold = QLineEdit(self)
        self.threshold.setToolTip('Input numeric value')
        self.threshold.move(500,100)
        self.threshold.resize(100,25)
        filterButton = QPushButton('Filter', self) 
        filterButton.setToolTip('Use button to filter the feature based on the chosen logic')
        #filterButton.clicked.connect(self.display_input)
        filterButton.move(700,100)
        filterButton.resize(50,50)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        #self.dialog = filterDialog(self)
        self.dialogs = list()
        
    # Main Window Init
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

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
        self.plot_menu.addAction('&Linear Regression', self.linearRegression)
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
        layout = QtWidgets.QVBoxLayout(self.main_widget)
        sc = MyMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        # Plot Button
        pbutton = QtWidgets.QPushButton('Plot')
        pbutton.clicked.connect(lambda: sc.update_figure(t, s, "XXX", "YYY"))
        # Toolbar Setup
        toolBar = NavigationToolbar(sc, self)

        layout.addWidget(sc)
        layout.addWidget(toolBar)
        layout.addWidget(pbutton)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Testing", 2000)

    """
    Define All Action Below
    """
    def fileOpen(self):
        self.close()

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
        
    def filterPrompt(self):
        dialog = filterDialog(self)
        self.dialogs.append(dialog)
        dialog.show()
        
    def dataPrompt(self):
        print("data")
        
    def linearRegression(self):
        dialog = linearRegressionDialog(self)
        self.dialogs.append(dialog)
        dialog.show()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", """Senior Design GUI prototype""")


if __name__ == '__main__':
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("Analysis Toolkit Prototype")
    aw.show()
    sys.exit(qApp.exec_())