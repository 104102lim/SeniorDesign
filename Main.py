from __future__ import unicode_literals
import sys

from PyQt5 import QtWidgets
import progressdialog as pgd

import applicationwindow as aw

if __name__ == '__main__':
    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    AW = aw.applicationWindow()
    AW.setWindowTitle("Analysis Toolkit Prototype")
    AW.loginPrompt()
    sys.exit(qApp.exec_())
