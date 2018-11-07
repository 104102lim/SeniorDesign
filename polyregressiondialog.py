from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QCompleter

from DatabasePreprocessing import getDescriptions

class polyRegressionDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(polyRegressionDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Polynomial Regression'
        self.left = 50
        self.top = 100
        self.width = 1200
        self.height = 120
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

        self.featureX = QComboBox(self)
        self.featureX.setToolTip('Select feature for X axis')
        self.featureX.move(15, 14)
        self.featureX.resize(840, 20)
        label = QLabel('X-Axis Feature', self)
        label.move(19, 16)
        label.resize(100, 50)
        self.featureY = QComboBox(self)
        self.featureY.setToolTip('Select feature for Y axis')
        self.featureY.move(15, 60)
        self.featureY.resize(840, 20)
        label = QLabel('Y-Axis Feature', self)
        label.move(19, 62)
        label.resize(100, 50)
        descriptions = getDescriptions()
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
        self.order.move(915, 14)
        self.order.resize(50,23)
        label = QLabel(' Order of\nPolynomial', self)
        label.move(906, 17)
        label.resize(120, 75)
        for i in range(1, 10):
            self.order.addItem(str(i))
        descriptions = getDescriptions()
        descriptions.sort()
        for d in descriptions:
            if (d != "bottom depth"
                    and d != "top depth"
                    and d != "Cost per unit"
                    and d != "Name of mud engineer"): continue
            self.featureY.addItem(d)
            self.featureX.addItem(d)
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot poly regression')
        plotButton.clicked.connect(self.parent().plotPolyRegression)
         plotButton.move(1020, 18)
        plotButton.resize(90, 90)