from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QCompleter
from DatabasePreprocessing import getDescriptions


class filterDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(filterDialog, self).__init__(parent)
        self.title = 'Filter Data'
        self.left = 500
        self.top = 50
        self.width = 1300
        self.height = 500
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
        
        descriptions = getDescriptions()
        self.counter = 0
        self.threshold = []
        self.feature1 = []
        self.feature2 = []
        self.logic = []
        self.addButton = QPushButton('+', self)
        self.addButton.move(1100, 80)
        self.addButton.clicked.connect(self.addExpression)
        self.filterButton = QPushButton('Filter', self)
        self.filterButton.move(1200, 80)
        
        for i in range(6):
            self.feature1.append(QComboBox(self))
            self.feature1[i].move(20, (i*60)+60)
            self.feature1[i].resize(840, 20)
            self.feature2.append(QComboBox(self))
            self.feature2[i].move(20, (i*60)+80)
            self.feature2[i].resize(840, 20)
            self.logic.append(QComboBox(self))
            self.logic[i].move(900, (i*60)+80)
            self.threshold.append(QLineEdit(self))
            self.threshold[i].move(1000, (i*60)+80)
            if i == 0:
                self.feature1[i].move(20, (i*40)+40)
                self.feature1[i].resize(840, 20)
                self.feature2[i].move(20, (i*40)+80)
                self.feature2[i].resize(840, 20)
                
                self.feature1[i].setInsertPolicy(QComboBox.NoInsert)
                self.feature1[i].setEditable(True)
                self.feature1[i].setCompleter(QCompleter(descriptions))
                self.feature1[i].completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
                self.label = QLabel('WHERE', self)
                self.label.move(400, 55)
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
        
    def addExpression(self):
        if(self.counter == 4):
            self.addButton.hide()
        if(self.counter < 5):
            self.counter += 1
            self.filterButton.move(1200, (60*self.counter) + 80)
            self.addButton.move(1100, (60*self.counter) + 80)
            self.feature2[self.counter].show()
            self.feature1[self.counter].show()
            self.logic[self.counter].show()
            self.threshold[self.counter].show()