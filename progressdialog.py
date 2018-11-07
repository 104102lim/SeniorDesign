from __future__ import unicode_literals
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QProgressBar, QComboBox, QLabel, QVBoxLayout
from PyQt5.QtCore import QBasicTimer, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox

class progressDialog(QMainWindow):
    def __init__(self, parent=None):
        super(progressDialog, self).__init__(parent)
        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint
        )

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Initialization')

        self.label1 = QLabel('DB Init:', self)
        self.label1.move(60, 20)
        self.label1.resize(70, 30)

        self.label2 = QLabel('Table Init: ', self)
        self.label2.move(60, 70)
        self.label2.resize(70, 30)

        self.label3 = QLabel('Tree Init: ', self)
        self.label3.move(60, 120)
        self.label3.resize(70, 30)

        self.label4 = QLabel('waiting', self)
        self.label4.move(140, 20)
        self.label4.resize(50, 30)

        self.label5 = QLabel('waiting', self)
        self.label5.move(140, 70)
        self.label5.resize(50, 30)

        self.label6 = QLabel('waiting', self)
        self.label6.move(140, 120)
        self.label6.resize(50, 30)


    def updateConnect(self):
        self.label4.setText("Done")

    def updateConnectFail(self):
        self.label4.setText("Fail")

    def updateTable(self):
        self.label5.setText("Done")

    def updateTree(self):
        self.label6.setText("Done")
