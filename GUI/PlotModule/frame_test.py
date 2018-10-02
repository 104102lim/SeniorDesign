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


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)

    # Main Window Init
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

    # Drop-down Menu Bar Setup
        # File Menu
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

        # Plot Menu (Assum it is the Linear Regression one)
        self.plot_menu = QtWidgets.QMenu('&Plot', self)

        self.lrBar = QtWidgets.QMenu('&Linear Regression', self)
        self.plot_menu.addMenu(self.lrBar)

        # Just add action like above
        # self.file_menu.addAction('&Something', self.something,
        #                                  QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.lrBar.addAction('&Option 1')
        self.lrBar.addAction('&Option 2')
        self.lrBar.addAction('&Option 3')
        self.lrBar.addAction('&Option 4')

        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.plot_menu)

        # View Menu (I assume it is the filter one)
        self.view_menu = QtWidgets.QMenu('&View', self)

        self.filterBar = QtWidgets.QMenu('&Filter', self)
        self.view_menu.addMenu(self.filterBar)
        # Just add action like above
        # self.file_menu.addAction('&Something', self.something,
        #                                  QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.filterBar.addAction('&Option 1')
        self.filterBar.addAction('&Option 2')
        self.filterBar.addAction('&Option 3')
        self.filterBar.addAction('&Option 4')
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.view_menu)

        # Help Menu
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

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", """Senior Design GUI prototype""")


if __name__ == '__main__':
    qApp = QtWidgets.QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.setWindowTitle("%s" % progname)
    aw.show()
    sys.exit(qApp.exec_())