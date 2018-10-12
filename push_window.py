'''
Created on Jul 11, 2018

@author: rg012f
'''


import sys
from PySide.QtGui  import * 
from PySide.QtCore import *
from PySide import QtGui
from PySide import QtCore


class PushWindow:

    wind_close_flg = False

    def __init__(self,last_parent):
        
        self.last_parent = last_parent
        
        self.main_widget = QWidget()
        self.main_widget.setMaximumHeight(400)
        
        self.parent_layout = QVBoxLayout()
        #self.last_parent.right_base_layout_v
        
        self.progress_bar_layout = QHBoxLayout()             #to incorporate the progress bar and the buttons
        
        self.secondary_progress_layout = QVBoxLayout()       #just the progress bar
        
        self.newfont = QtGui.QFont("Verdana", 10, QtGui.QFont.Normal)
        
        self.push_layout = QVBoxLayout()
        
        self.push_textbox = QPlainTextEdit()
        self.push_textbox.setFont(self.newfont)
        self.push_textbox.setStyleSheet("background-color: black ;color:white;border: 2px blue; ")
        self.push_textbox.setReadOnly(True)
        self.push_layout.addWidget(self.push_textbox)
    
        self.progress_bar_layout.addLayout(self.secondary_progress_layout)

        
        self.parent_layout.addLayout(self.push_layout)
        self.parent_layout.addLayout(self.progress_bar_layout)
        
        
        self.progressBar = QtGui.QProgressBar()
        self.progressLabel =  QtGui.QLabel("Push process is in progress .... Please wait until the process is completed...!")
        self.cancel_button = QtGui.QPushButton("Cancel")
        
        self.progressBar.setProperty("Current status", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMaximumHeight(15)
        self.progressBar.setTextVisible(True)
        self.progressBar.setValue(0)
        
        
        self.progressLabel.setFont(self.newfont)
        
        self.secondary_progress_layout.addWidget(self.progressBar)
        self.secondary_progress_layout.addWidget(self.progressLabel)
        self.progress_bar_layout.addWidget(self.cancel_button)
# self.last_parent.msgBox.information(,'Job status!',"Ping logs process has  been closed.!", QtGui.QMessageBox.Ok)
        
        self.main_widget.setLayout(self.parent_layout) 
        
           
        self.last_parent.right_base_layout_v.addWidget(self.main_widget)
        
        self.main_widget.hide()
        
    def prepare_window(self,):
        print("i have reached prepare window for push")
        self.progressBar.show()
        self.progressLabel.show()
        self.cancel_button.show()
#Container Widget
        self.push_textbox.clear()
        self.main_widget.show()
        
    def closeEvent(self,event):
        
       
        self.wind_close_flg = True