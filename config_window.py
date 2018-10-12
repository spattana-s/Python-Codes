'''
Created on Jul 7, 2018

@author: rg012f
'''
import sys
from PySide.QtGui  import * 
from PySide.QtCore import *
from PySide import QtGui
from PySide import QtCore


class ConfigWindow:

    wind_close_flg = False

    def __init__(self,last_parent):
        
        self.last_parent = last_parent
        
        self.main_widget = QWidget()
        self.main_widget.setMaximumHeight(400)
        
        self.parent_layout = QVBoxLayout()
        #self.last_parent.right_base_layout_v
        
        self.progress_bar_layout = QHBoxLayout()             #to incorporate the progress bar and the buttons
        
        self.secondary_progress_layout = QVBoxLayout()       #just the progress bar
        
        self.control_button_layout = QGridLayout()           #cancel,close,open valid / invalid file

        
        self.config_layout = QVBoxLayout()
        
        self.config_textbox = QPlainTextEdit()
        self.config_textbox.setFont(QtGui.QFont("Verdana", 10, QtGui.QFont.Bold))
        self.config_textbox.setReadOnly(True)
        self.config_layout.addWidget(self.config_textbox)
    
        self.progress_bar_layout.addLayout(self.secondary_progress_layout)
        self.progress_bar_layout.addLayout(self.control_button_layout)

        
        self.parent_layout.addLayout(self.config_layout)
        self.parent_layout.addLayout(self.progress_bar_layout)
        
        
        self.progressBar = QtGui.QProgressBar()
        self.progressLabel =  QtGui.QLabel("Configuration process is in progress .... Please wait until the log file is generated...!")
        self.cancel_button = QtGui.QPushButton("Cancel")
        
        self.progressBar.setProperty("Current status", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMaximumHeight(15)
        self.progressBar.setTextVisible(True)
        self.progressBar.setValue(0)
        
        
        self.progressLabel.setFont(QtGui.QFont("verdana", 9, QtGui.QFont.Normal))
        
        self.secondary_progress_layout.addWidget(self.progressBar)
        self.secondary_progress_layout.addWidget(self.progressLabel)
        self.progress_bar_layout.addWidget(self.cancel_button)
# self.last_parent.msgBox.information(,'Job status!',"Ping logs process has  been closed.!", QtGui.QMessageBox.Ok)
        
        self.main_widget.setLayout(self.parent_layout) 
        
           
        self.last_parent.right_base_layout_v.addWidget(self.main_widget)
        
        self.main_widget.hide()
        
    def prepare_window(self,):
        print("i have reached prepare window for configs")
        self.progressBar.show()
        self.progressLabel.show()
        self.cancel_button.show()
#Container Widget
        self.config_textbox.clear()
        self.main_widget.show()
        
    def closeEvent(self,event):
        
       
        self.wind_close_flg = True
    
        