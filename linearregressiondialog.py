from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QCheckBox, QCompleter

from DatabasePreprocessing import getDescriptions


class linearRegressionDialog(QtWidgets.QMainWindow):
       def __init__(self, parent=None):
        super(linearRegressionDialog, self).__init__(parent)
        self.title = 'Linear Regression'
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
        label.move(18, 20)
        label.resize(100, 50)
        self.featureY = QComboBox(self)
        self.featureY.setToolTip('Select feature for Y axis')
        self.featureY.move(15, 60)
        self.featureY.resize(840, 20)
        label = QLabel('Y-Axis Feature', self)
        label.move(20, 62)
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
        self.yIntercept = QCheckBox("Y-Intercept", self)
        self.yIntercept.move(880, 10)
        self.rSquared = QCheckBox("R^2", self)
        self.rSquared.move(880, 40)
        self.slopeCheck = QCheckBox("Slope", self)
        self.slopeCheck.move(880, 70)
        plotButton = QPushButton('Plot', self)
        plotButton.setToolTip('Use button to plot linear regression')
        plotButton.clicked.connect(self.parent().plotLinearRegression)
        plotButton.move(1020, 18)
        plotButton.resize(90, 90)