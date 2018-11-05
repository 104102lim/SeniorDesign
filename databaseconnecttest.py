from __future__ import unicode_literals
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit
import pyodbc

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
        label = QLabel('Port (Optional)', self)
        label.move(80, 100)
        label.resize(150, 30)
        self.port = QLineEdit(self)
        self.port.setToolTip('Enter Port (Optional)')
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
        label = QLabel('Instance', self)
        label.move(80, 260)
        label.resize(150, 30)
        self.instance = QLineEdit(self)
        self.instance.setToolTip('Instance')
        self.instance.move(200, 260)
        self.instance.resize(130, 30)
        enterButton = QPushButton('Login', self)
        enterButton.setToolTip('Login')
        enterButton.clicked.connect(self.login)
        enterButton.move(224, 300)
        enterButton.resize(80, 50)
     
    def login(self):
        server = str(self.server.text())
        portLog = str(self.port.text())
        dbName = str(self.databaseName.text())
        UID = str(self.username.text())
        PWD = str(self.password.text())
        instance = str(self.instance.text())
        try:
            if portLog != '' and instance != '':
                cnxn = pyodbc.connect(
                    "DRIVER={SQL Server}; SERVER=" + server + "\\" + instance + "," + portLog + ";" +
                    " DATABASE=" + dbName + "; UID = " + UID + "; PWD = " + PWD)
                cursor = cnxn.cursor()
            elif portLog != '':
                cnxn = pyodbc.connect(
                    "DRIVER={SQL Server}; SERVER=" + server + "," + portLog + ";" +
                    " DATABASE=" + dbName + "; UID = " + UID + "; PWD = " + PWD)
                cursor = cnxn.cursor()
            elif instance != '':
                cnxn = pyodbc.connect(
                    "DRIVER={SQL Server}; SERVER=" + server + "\\" + instance + ";" +
                    " DATABASE=" + dbName + "; UID = " + UID + "; PWD = " + PWD)
                cursor = cnxn.cursor()
            else:
                cnxn = pyodbc.connect(
                    "DRIVER={SQL Server}; SERVER=" + server + ";" +
                    " DATABASE=" + dbName + "; UID = " + UID + "; PWD = " + PWD)
                cursor = cnxn.cursor()
            print("Success")
        except Exception as e:
            print("Failure")
            
        

if __name__ == '__main__':
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    LG = loginDialog()
    LG.setWindowTitle("Login Window")
    LG.show()
    sys.exit(qApp.exec_())
