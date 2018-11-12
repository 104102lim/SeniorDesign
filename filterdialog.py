from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QCompleter
from DatabasePreprocessing import getDescriptions


class filterDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(filterDialog, self).__init__(parent)
        self.title = 'Filter Data'
        self.left = 200
        self.top = 50
        self.width = 1450
        self.height = 800
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
        self.addButton.move(1175, 100)
        self.addButton.clicked.connect(self.addExpression)
        self.filterButton = QPushButton('Filter', self)
        self.filterButton.move(1300, 100)
        self.filterButton.clicked.connect(self.parent().filterData)
        
        for i in range(6):
            self.feature1.append(QComboBox(self))
            self.feature1[i].move(400, (i*120)+60)
            self.feature1[i].resize(50, 20)
            self.feature2.append(QComboBox(self))
            self.feature2[i].move(20, (i*120)+100)
            self.feature2[i].resize(840, 20)
            self.logic.append(QComboBox(self))
            self.logic[i].move(890, (i*120)+100)
            self.logic[i].resize(115, 30)
            self.threshold.append(QLineEdit(self))
            self.threshold[i].move(1025, (i*120)+100)
            self.threshold[i].resize(125,30)
            if i == 0:
                self.feature1[i].move(20, (i*80)+40)
                self.feature1[i].resize(840, 20)
                self.feature2[i].move(20, (i*80)+100)
                self.feature2[i].resize(840, 20)
                
                self.feature1[i].setInsertPolicy(QComboBox.NoInsert)
                self.feature1[i].setEditable(True)
                self.feature1[i].setCompleter(QCompleter(descriptions))
                self.feature1[i].completer().setCompletionMode(QCompleter.UnfilteredPopupCompletion)
                self.label = QLabel('WHERE', self)
                self.label.move(400, 60)
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
            #self.addButton.move(80, 2000)
            self.addButton.hide()
            #self.filterButton.move(800,(60*self.counter) + 80)
            #self.filterButton.resize(200,50)
        if(self.counter < 5):
            self.counter += 1
            self.filterButton.move(1300, (120*self.counter) + 100)
            self.addButton.move(1175, (120*self.counter) + 100)
            self.feature2[self.counter].show()
            self.feature1[self.counter].show()
            self.logic[self.counter].show()
            self.threshold[self.counter].show()