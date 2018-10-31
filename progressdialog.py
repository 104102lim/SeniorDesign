from __future__ import unicode_literals
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QBasicTimer

class progressDialog(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('ProgressBar')
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        # self.button = QPushButton('Start', self)
        # self.button.setFocusPolicy(Qt.NoFocus)
        # self.button.move(40, 80)
        #
        # self.button.clicked.connect(self.onStart)
        self.timer = QBasicTimer()
        self.step = 0

        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)
