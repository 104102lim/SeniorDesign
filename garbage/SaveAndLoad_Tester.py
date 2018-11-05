
from PyQt5.QtWidgets import QApplication, QProgressBar, QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QBasicTimer


class ProgressBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('ProgressBar')
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.step = 0
        self.pbar.setValue(self.step)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    qb = ProgressBar()
    qb.show()
    sys.exit(app.exec_())