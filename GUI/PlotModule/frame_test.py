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
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

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
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
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

        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Import', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_I)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        # Canvas Setup
        layout = QtWidgets.QVBoxLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
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