from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QCompleter
from DatabasePreprocessing import getDescriptions


class filterDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(filterDialog, self).__init__(parent)
        self.title = 'Filter Data'
        self.left = 500
        self.top = 50
        self.width = 800
        self.height = 400
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

        self.counter = 0
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.vLayout = QVBoxLayout(self.centralWidget)

        descriptions = getDescriptions()
        self.buttonsWidget = []
        self.buttonsWidgetLayout = []
        self.threshold = []
        self.feature1 = []
        self.feature2 = []
        self.logic = []
        for i in range(6):
            self.buttonsWidget.append(QWidget())
            self.buttonsWidgetLayout.append(QHBoxLayout(self.buttonsWidget[i]))
            self.threshold.append(QLineEdit(self))
            self.logic.append(QComboBox(self))
            self.feature1.append(QComboBox(self))
            self.feature2.append(QComboBox(self))
            if i == 0:
                self.feature1[i].setInsertPolicy(QComboBox.NoInsert)
                self.feature1[i].setEditable(True)
                self.feature1[i].setCompleter(QCompleter(descriptions))
                self.feature1[i].completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
            else:
                self.threshold[i].hide()
                self.feature1[i].hide()
                self.feature2[i].hide()
                self.logic[i].hide()
            self.feature2[i].setInsertPolicy(QComboBox.NoInsert)
            self.feature2[i].setEditable(True)
            self.feature2[i].setCompleter(QCompleter(descriptions))
            self.feature2[i].completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        operators = ["AND", "OR"]
        for i in range(1, len(self.threshold)):
            for p in operators:
                self.feature1[i].addItem(p)
        logics = ["=", "!=", "<", ">", "<=", ">=", "Contains", "Does Not Contain"]
        for i in range(len(self.logic)):
            for l in logics:
                self.logic[i].addItem(l)
        self.addButton = QPushButton('+', self)
        self.addButton.clicked.connect(self.addExpression)
        filterButton = QPushButton('Filter', self)
        filterButton.setToolTip('Use button to filter the feature based on the chosen logic')
        filterButton.clicked.connect(self.parent().filterData)

        for i in range(6):
            self.buttonsWidgetLayout[i].addWidget(self.feature1[i])
            self.buttonsWidgetLayout[i].addWidget(self.feature2[i])
            self.buttonsWidgetLayout[i].addWidget(self.logic[i])
            self.buttonsWidgetLayout[i].addWidget(self.threshold[i])
            self.buttonsWidgetLayout[i].addWidget(self.addButton)
            self.buttonsWidgetLayout[i].addWidget(filterButton)
            self.vLayout.addWidget(self.buttonsWidget[i])

        self.left2 = 0
        self.top2 = 0
        self.width2 = 800
        self.height2 = 50
        #self.vLayout.setGeometry(self,self.left2, self.top2, self.width2, self.height2)
        #self.buttonsWidget[0].setParent(None)
            
    def addExpression(self):
        if(self.counter == 4):
            self.addButton.hide()
        if(self.counter < 5):
            self.counter += 1
            self.feature2[self.counter].show()
            self.feature1[self.counter].show()
            self.logic[self.counter].show()
            self.threshold[self.counter].show()
            # self.buttonsWidgetLayout[self.counter + 1].addWidget(self.feature1[self.counter + 1])
            # self.buttonsWidgetLayout[self.counter + 1].addWidget(self.feature2[self.counter + 1])
            # self.buttonsWidgetLayout[self.counter + 1].addWidget(self.logic[self.counter + 1])
            # self.buttonsWidgetLayout[self.counter + 1].addWidget(self.threshold[self.counter + 1])
            # self.vLayout.addWidget(self.buttonsWidget[self.counter + 1])
