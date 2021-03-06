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
        label = QLabel('Machine Name or IP', self)
        label.move(60, 60)
        label.resize(150, 30)
        self.server = QLineEdit(self)
        self.server.setToolTip('Enter Machine Name or IP')
        self.server.move(220, 60)
        self.server.resize(130, 30)
        label = QLabel('Port or Instance Name\n(Optional)', self)
        label.move(60, 100)
        label.resize(150, 30)
        self.port = QLineEdit(self)
        self.port.setToolTip('Enter Port or Instance Name\n(Optional)')
        self.port.move(220, 100)
        self.port.resize(130, 30)
        label = QLabel('Database Name', self)
        label.move(60, 140)
        label.resize(150, 30)
        self.databaseName = QLineEdit(self)
        self.databaseName.setToolTip('Enter Database Name')
        self.databaseName.move(220, 140)
        self.databaseName.resize(130, 30)
        label = QLabel('Username', self)
        label.move(60, 180)
        label.resize(150, 30)
        self.username = QLineEdit(self)
        self.username.setToolTip('Enter Username')
        self.username.move(220, 180)
        self.username.resize(130, 30)
        label = QLabel('Password', self)
        label.move(60, 220)
        label.resize(150, 30)
        self.password = QLineEdit(self)
        self.password.setToolTip('Enter Password')
        self.password.move(220, 220)
        self.password.resize(130, 30)
        enterButton = QPushButton('Login', self)
        enterButton.setToolTip('Login')
        enterButton.clicked.connect(self.login)
        enterButton.move(245, 260)
        enterButton.resize(80, 50)
     
    def login(self):
        server = str(self.server.text())
        port = str(self.port.text())
        dbName = str(self.databaseName.text())
        UID = str(self.username.text())
        PWD = str(self.password.text())
        try:
            if port == '':
                cnxn = pyodbc.connect(
                    "DRIVER={SQL Server}; SERVER=" + server + ";" +
                    " DATABASE=" + dbName + "; UID = " + UID + "; PWD = " + PWD)
            else:
                try:
                    p = int(port)
                except:
                    p = port
            if type(p) is int:
                cnxn = pyodbc.connect(
                    "DRIVER={SQL Server}; SERVER=" + server + "," + p + ";" +
                    " DATABASE=" + dbName + "; UID = " + UID + "; PWD = " + PWD)
            elif type(p) is str:
                cnxn = pyodbc.connect(
                    "DRIVER={SQL Server}; SERVER=" + server + "\\" + p + ";" +
                    " DATABASE=" + dbName + "; UID = " + UID + "; PWD = " + PWD)
            QtWidgets.QMessageBox.about(self, "Success!", """Success!""")
        except Exception as e:
            with open("LoginLog.txt", mode="w") as f:
                f.write(str(e))
            QtWidgets.QMessageBox.about(self, "Failure!", """Failure!""")
        self.close()

if __name__ == '__main__':
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    LG = loginDialog()
    LG.setWindowTitle("Login Window")
    LG.show()
    sys.exit(qApp.exec_())
