'''
Created on 8 June  2018

@author: sp977u@att.com  (Satish Palnati)

'''
import sys
from PySide.QtGui  import * 
from PySide.QtCore import *
from PySide import QtGui
from PySide import QtCore
import os
from views.common.left_base_view import left_base
from views.compare_window.compare_window import CompareWindow
class compare_op_results:

    def __init__(self,last_parent):
        
        self.last_parent = last_parent
        self.draw_compare_portion()
        
    def draw_compare_portion(self):

        self.main_widget = QWidget()
        
#     def draw_compare_portion(self):
        
        self.file_list = []
        self.Routers_Switches_options_list = ["Interface Status", "VLANs Information" , "OSPF Neighbors","Route Table", "VRF Ping and Trace", "Route Summary"]
        self.FW_options_list = ["FW Route Table" ,  "FW ACL Hits" , "BSO FW AAA" , "FW Local NAT" , "FW Global NAT"]
        self.BGP_options_list = [ "BGP Neighbors", "BGP ADVT Routes" , "BGP Received Routes" , "BGP Route ATTR" , "BGP Neighbor prefix Changes" , "BGP Neighbor state Changes"   ]
        
        self.newfont = QtGui.QFont("Verdana", 10, QtGui.QFont.Normal)
        
        
        self.parent_layout_v = QVBoxLayout()
        
        self.file_selection_layout_h = QHBoxLayout()
        self.parent_layout_v.addLayout(self.file_selection_layout_h)             #to incorporate the file select buttons
        self.base_log_file_layout_v = QVBoxLayout()
        self.file_selection_layout_h.addLayout(self.base_log_file_layout_v)
        
        self.base_log_file_label =  QtGui.QLabel()
        self.base_log_file_label.setText("Select Base Log file" )
        self.base_log_file_label.setFont(self.newfont)
        self.base_log_file_layout_v.addWidget(self.base_log_file_label)
        self.base_log_file_label.hide()
        
        self.base_log_file_btn = QtGui.QPushButton("Open")
        self.base_log_file_btn.setMinimumWidth(100)
        self.base_log_file_btn.setMaximumWidth(100)
        self.base_log_file_btn.setFont(self.newfont)
        self.base_log_file_btn.setObjectName("Select")
        self.base_log_file_btn.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.base_log_file_btn.setToolTip("Please click to open base log file !")
        self.base_log_file_layout_v.addWidget(self.base_log_file_btn)
        self.base_log_file_btn.hide()
        
        self.vs_layout_h = QHBoxLayout()
        self.file_selection_layout_h.addLayout(self.vs_layout_h)
        self.vs_layout_h.setAlignment(QtCore.Qt.AlignCenter)
        self.vs_label =  QtGui.QLabel("V/S")
        self.vs_layout_h.addWidget(self.vs_label)
        self.vs_label.hide()
                
        self.new_log_file_layout_v = QVBoxLayout()
        self.file_selection_layout_h.addLayout(self.new_log_file_layout_v)
        
        self.new_log_file_label =  QtGui.QLabel()
        self.new_log_file_label.setText("Select New Log file" )
        self.new_log_file_label.setFont(self.newfont)
        self.new_log_file_layout_v.addWidget(self.new_log_file_label)
        self.new_log_file_label.hide()
        
        self.new_log_file_btn = QtGui.QPushButton("Open")
        self.new_log_file_btn.setMinimumWidth(100)
        self.new_log_file_btn.setMaximumWidth(100)
        self.new_log_file_btn.setFont(self.newfont)
        self.new_log_file_btn.setObjectName("Select")
        self.new_log_file_btn.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.new_log_file_btn.setToolTip("Please click to open new log file !")
        self.new_log_file_layout_v.addWidget(self.new_log_file_btn)
        self.new_log_file_btn.hide()
        
        
        
        self.RS_CheckBox = [QtGui.QCheckBox() for _ in range(len(self.Routers_Switches_options_list))]
        self.RS_CheckBox_layout_v = QVBoxLayout()

        i = 0
        for RS in self.RS_CheckBox:
            RS.setText(self.Routers_Switches_options_list[i])
            self.RS_CheckBox_layout_v.addWidget(RS)
            i += 1
        
        self.FW_CheckBox = [QtGui.QCheckBox() for _ in range(len(self.FW_options_list))]
        self.FW_CheckBox_layout_v = QVBoxLayout()

        i = 0
        for FW in self.FW_CheckBox:
            FW.setText(self.FW_options_list[i])
            self.FW_CheckBox_layout_v.addWidget(FW)
            i += 1
            
            
        self.BGP_CheckBox = [QtGui.QCheckBox() for _ in range(len(self.BGP_options_list))]
        self.BGP_CheckBox_layout_v = QVBoxLayout()

        i = 0
        for BGP in self.BGP_CheckBox:
            BGP.setText(self.BGP_options_list[i])
            self.BGP_CheckBox_layout_v.addWidget(BGP)
            i += 1


        self.groupBox_layout_h = QHBoxLayout()
        
        self.groupBox_layout_h.addLayout(self.RS_CheckBox_layout_v)
        self.groupBox_layout_h.addLayout(self.FW_CheckBox_layout_v)
        self.groupBox_layout_h.addLayout(self.BGP_CheckBox_layout_v)
        
        self.checkbox_groupBox = QtGui.QGroupBox("Compare Attributes")
        self.checkbox_groupBox.setToolTip("Please Select at least ONE attribute from the given check-boxes to compare logs")
        self.checkbox_groupBox.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.checkbox_groupBox.setLayout(self.groupBox_layout_h)
        self.parent_layout_v.addWidget(self.checkbox_groupBox)
        
        
        self.main_widget.setLayout(self.parent_layout_v) 
           
        self.last_parent.right_base_layout_v.addWidget(self.main_widget)
        
        self.main_widget.hide()
        
    def display_comapre_portion(self):
        
        self.last_parent.credentials_groupbox.show()
        self.last_parent.IP_groupBox.show()
        self.last_parent.Commands_groupBox.show()
        self.last_parent.results_groupBox.show()
        self.last_parent.base_left.show_left_common()
        
        self.base_log_file_btn.show()
        self.base_log_file_btn.show()
        self.vs_label.show()
        self.new_log_file_label.show()
        self.new_log_file_btn.show()
        self.main_widget.show()
   
        self.last_parent.base_left.go_button.show()
        self.last_parent.base_left.go_button.setText("Compare")
        
        
    
    
        
        
              
        
        