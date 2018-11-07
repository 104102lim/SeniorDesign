from __future__ import unicode_literals
import sys

from PyQt5 import QtWidgets

import applicationwindow as aw

if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook

    qapp = 0
    qApp = QtWidgets.QApplication(sys.argv)
    AW = aw.applicationWindow()
    AW.setWindowTitle("Analysis Toolkit Prototype")
    AW.loginPrompt()
    sys.exit(qApp.exec_())
