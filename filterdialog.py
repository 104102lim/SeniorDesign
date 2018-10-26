from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

class filterDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(filterDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.title = 'Filter Data'
        self.left = 500
        self.top = 50
        self.width = 800
        self.height = 300
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())

        self.counter = 0
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.vLayout = QVBoxLayout(self.centralWidget)

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
            self.feature1.append(QComboBox(self))
            self.feature2.append(QComboBox(self))
            self.logic.append(QComboBox(self))

        addButton = QPushButton('+', self)
        addButton.clicked.connect(self.addExpression)
        filterButton = QPushButton('Filter', self)
        filterButton.setToolTip('Use button to filter the feature based on the chosen logic')
        filterButton.clicked.connect(self.parent().filterData)
        
        self.buttonsWidgetLayout[0].addWidget(self.feature1[0])
        self.buttonsWidgetLayout[0].addWidget(self.feature2[0])
        self.buttonsWidgetLayout[0].addWidget(self.logic[0])
        self.buttonsWidgetLayout[0].addWidget(self.threshold[0])
        self.buttonsWidgetLayout[0].addWidget(addButton)
        self.buttonsWidgetLayout[0].addWidget(filterButton)
        
        
        self.vLayout.addWidget(self.buttonsWidget[0])
            
    def addExpression(self):
        if(self.counter < 5):
            self.buttonsWidgetLayout[self.counter + 1].addWidget(self.feature1[self.counter + 1])
            self.buttonsWidgetLayout[self.counter + 1].addWidget(self.feature2[self.counter + 1])
            self.buttonsWidgetLayout[self.counter + 1].addWidget(self.logic[self.counter + 1])
            self.buttonsWidgetLayout[self.counter + 1].addWidget(self.threshold[self.counter + 1])
            self.vLayout.addWidget(self.buttonsWidget[self.counter + 1])
            self.counter += 1
        else:
            pass

