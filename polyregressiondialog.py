from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QCompleter

from DatabasePreprocessing import getDescriptions

class polyRegressionDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(polyRegressionDialog, self).__init__(parent)
        self.title = 'Poly Regression'
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

        label = QLabel('Poly Regression', self)
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
        self.order = QComboBox(self)
        self.order.setToolTip('Select order of polynomial fit')
        self.order.move(450, 100)
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
        plotButton.move(700, 100)
        plotButton.resize(50, 50)