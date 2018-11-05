from __future__ import unicode_literals
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QProgressBar, QComboBox
from PyQt5.QtCore import QBasicTimer


class progressDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(progressDialog, self).__init__(parent)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Initializing')
        QComboBox(self)
