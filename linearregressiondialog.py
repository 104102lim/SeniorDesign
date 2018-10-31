from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QCheckBox, QCompleter

from DatabasePreprocessing import getDescriptions

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

        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        label = QLabel('Linear Regression', self)
        label.move(20, 90)
        label.resize(250, 50)
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
        self.yIntercept = QCheckBox("Y-Intercept", self)
        self.yIntercept.move(450, 100)
        self.rSquared = QCheckBox("R^2", self)
        self.rSquared.move(550, 100)
        self.slopeCheck = QCheckBox("Slope", self)
        self.slopeCheck.move(600, 100)
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot linear regression')
        plotButton.clicked.connect(self.parent().plotLinearRegression)
        plotButton.move(700, 100)
        plotButton.resize(50, 50)
