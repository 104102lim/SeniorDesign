from __future__ import unicode_literals
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit

class loginDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(loginDialog, self).__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.title = 'User Login'
        self.left = 200
        self.top = 100
        self.width = 450
        self.height = 370
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())
        # input boxes and labels
        label = QLabel('Machine Name/IP', self)
        label.move(80, 60)
        label.resize(150, 30)
        self.server = QLineEdit(self)
        self.server.setToolTip('Enter Machine Name/IP')
        self.server.move(200, 60)
        self.server.resize(130, 30)
        label = QLabel('Port/Instance', self)
        label.move(80, 100)
        label.resize(150, 30)
        self.port = QLineEdit(self)
        self.port.setToolTip('Enter Port/Instance')
        self.port.move(200, 100)
        self.port.resize(130, 30)
        label = QLabel('Database Name', self)
        label.move(80, 140)
        label.resize(150, 30)
        self.databaseName = QLineEdit(self)
        self.databaseName.setToolTip('Enter Database Name')
        self.databaseName.move(200, 140)
        self.databaseName.resize(130, 30)
        label = QLabel('Username', self)
        label.move(80, 180)
        label.resize(150, 30)
        self.username = QLineEdit(self)
        self.username.setToolTip('Enter Username')
        self.username.move(200, 180)
        self.username.resize(130, 30)
        label = QLabel('Password', self)
        label.move(80, 220)
        label.resize(150, 30)
        self.password = QLineEdit(self)
        self.password.setToolTip('Enter Password')
        self.password.move(200, 220)
        self.password.resize(130, 30)
        enterButton = QPushButton('Login', self)
        enterButton.setToolTip('Login')
        enterButton.clicked.connect(self.parent().login)
        enterButton.move(224, 260)
        enterButton.resize(80, 50)