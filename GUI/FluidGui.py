#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 17:12:52 2018

@author: JoeyGallardo
"""
import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QMenu
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('File')
        impMenu = QMenu('Run', self)
        impAct = QAction('Plot Graph', self) 
        impMenu.addAction(impAct)
     
        fileMenu.addMenu(impMenu)

        fileMenu.addAction(exitAct)
       
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Simple Gui Menu')    
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
