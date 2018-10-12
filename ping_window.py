'''
Created on 17 june, 2018
@author: sp977u@att.com  (Satish Palnati)
This class is for 

'''
import sys
from PySide.QtGui  import * 
from PySide.QtCore import *
from PySide import QtGui
from PySide import QtCore

class PingWindow:

    wind_close_flg = False

    def __init__(self,last_parent):
        
        self.last_parent = last_parent

        self.main_widget = QWidget()
        self.main_widget.setMaximumHeight(400)
        
        self.parent_layout = QVBoxLayout()
        #self.last_parent.right_base_layout_v

        
        self.ping_log_layout = QHBoxLayout()
        
        self.progress_bar_layout = QHBoxLayout()             #to incorporate the progress bar and the buttons
        
        self.secondary_progress_layout = QVBoxLayout()       #just the progress bar
        
        self.control_button_layout = QGridLayout()           #cancel,close,open valid / invalid file
                        
                        
        # UP ip layout for ping logs                
        self.up_ip_layout = QVBoxLayout()
        
        self.up_ip_btn = QtGui.QLabel("UP Nodes")
        self.up_ip_btn.setFont(QtGui.QFont("Verdana", 10, QtGui.QFont.Bold))
        self.up_ip_btn.setStyleSheet("background-color:white ;color:Green;border: 2px solid black")
        self.up_ip_layout.addWidget(self.up_ip_btn)
        
        self.up_ip_btn.setToolTip("Please click here to open UP NODE file.. !")
        self.up_ip_btn.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")

        self.up_ip_textbox = QPlainTextEdit()
        self.up_ip_textbox.setFont(QtGui.QFont("Verdana", 10, QtGui.QFont.Bold))
        self.up_ip_textbox.setStyleSheet("background-color: rgb(150,240,190) ;color:rgb(9,57,31);border: 2px solid black; ")
        self.up_ip_textbox.setReadOnly(True)
        self.up_ip_layout.addWidget(self.up_ip_textbox)
        
        # DOWN ip layout for ping logs
        self.down_ip_layout = QVBoxLayout()
        
        self.down_ip_btn = QtGui.QLabel("DOWN Nodes")
        self.down_ip_btn.setFont(QtGui.QFont("Verdana", 10, QtGui.QFont.Bold))
        self.down_ip_btn.setStyleSheet("QPushButton {background-color: white ;color:Red;border: 2px solid black}")
        self.down_ip_layout.addWidget(self.down_ip_btn)
        
        self.down_ip_btn.setToolTip("Please click here to open UP NODE file.. !")
        self.down_ip_btn.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        
        self.down_ip_textbox = QPlainTextEdit()
        self.down_ip_textbox.setFont(QtGui.QFont("Verdana", 10, QtGui.QFont.Bold))
        self.down_ip_textbox.setStyleSheet("background-color: rgb(250,210,210);color:rgb(118,14,16);border: 2px solid black; ")
        self.down_ip_textbox.setReadOnly(True)
        self.down_ip_layout.addWidget(self.down_ip_textbox)
    
        self.progress_bar_layout.addLayout(self.secondary_progress_layout)
        self.progress_bar_layout.addLayout(self.control_button_layout)
        
        self.ping_log_layout.addLayout(self.up_ip_layout)
        self.ping_log_layout.addLayout(self.down_ip_layout)
        
        self.parent_layout.addLayout(self.ping_log_layout)
        self.parent_layout.addLayout(self.progress_bar_layout)
        
        
        self.progressBar = QtGui.QProgressBar()
        self.progressLabel =  QtGui.QLabel("Ping process is in progress .... Please wait until the log file is generated...!")
        self.cancel_button = QtGui.QPushButton("Cancel")
        
#         self.progressBar.setGeometry(QtCore.QRect(100, 645, 710, 17))
        self.progressBar.setProperty("Current status", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMaximumHeight(15)
        self.progressBar.setTextVisible(True)
        self.progressBar.setValue(0)
        self.progressBar.setRange(0,100)
        
        
        self.progressLabel.setFont(QtGui.QFont("verdana", 9, QtGui.QFont.Normal))
        
        self.secondary_progress_layout.addWidget(self.progressBar)
        self.secondary_progress_layout.addWidget(self.progressLabel)
        self.progress_bar_layout.addWidget(self.cancel_button)
       # self.last_parent.msgBox.information(,'Job status!',"Ping logs process has  been closed.!", QtGui.QMessageBox.Ok)
        
        self.main_widget.setLayout(self.parent_layout) 
        
           
        self.last_parent.right_base_layout_v.addWidget(self.main_widget)
        
        self.main_widget.hide()
        
  
    def prepare_window(self,):
 
        self.progressBar.show()
        self.progressLabel.show()
        self.cancel_button.show()
        self.up_ip_textbox.clear()
        self.down_ip_textbox.clear()
        self.main_widget.show()
        
    def closeEvent(self,event):
        
       
        self.wind_close_flg = True
        
    
        