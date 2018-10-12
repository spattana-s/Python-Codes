'''
Created on 1 june, 2018

@author: sp977u@att.com  (Satish Palnati)

'''
from PySide import QtGui
from PySide import QtCore
import os

from PySide.QtGui import QWidget,QFrame

class extract_excel:

    def __init__(self,gui,left_common):
        
        self.gui = gui
        self.left_common = left_common
        
        self.excel_disp_flag = False
        self.draw_excel_portion()
        
        
    def draw_excel_portion(self):
        
        self.newfont = QtGui.QFont("Verdana", 8, QtGui.QFont.Normal)
        
        self.userOptionextract = QtGui.QTabWidget(self.gui)
        self.userOptionextract.setTabShape(QtGui.QTabWidget.Rounded)
        self.userOptionextract.setElideMode(QtCore.Qt.ElideNone)
        self.userOptionextract.setObjectName("tabWidget")
        
        self.left_common.last_parent.right_base_layout_v.addWidget(self.userOptionextract)
       
        
        
        self.generalTab = QtGui.QWidget()
        self.generalTab.setObjectName("general")
            
        self.userOptionextract.addTab(self.generalTab,"General") 
        self.userOptionextract.setFont(self.newfont)
        
        self.hostNameChbx = QtGui.QCheckBox(self.generalTab)
        self.hostNameChbx.setGeometry(QtCore.QRect(15, 25, 145, 22))
        self.hostNameChbx.setFont(self.newfont)
        self.hostNameChbx.setObjectName("Hostname")
        self.hostNameChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.hostNameChbx.setText(" Hostname : ")
        
        self.ipaddChbx = QtGui.QCheckBox(self.generalTab)
        self.ipaddChbx.setGeometry(QtCore.QRect(15, 70, 145, 22))
        self.ipaddChbx.setFont(self.newfont)
        self.ipaddChbx.setObjectName("ipadd")
        self.ipaddChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.ipaddChbx.setText(" IP Address : ")
        
        self.modelChbx = QtGui.QCheckBox(self.generalTab)
        self.modelChbx.setGeometry(QtCore.QRect(15, 115, 145, 22))
        self.modelChbx.setFont(self.newfont)
        self.modelChbx.setObjectName("model")
        self.modelChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.modelChbx.setText("Model : ")
        
        self.osversionChbx = QtGui.QCheckBox(self.generalTab)
        self.osversionChbx.setGeometry(QtCore.QRect(15, 155, 145, 22))
        self.osversionChbx.setFont(self.newfont)
        self.osversionChbx.setObjectName("osver")
        self.osversionChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.osversionChbx.setText(" OS Version : ")
        
        self.templateVerChbx = QtGui.QCheckBox(self.generalTab)
        self.templateVerChbx.setGeometry(QtCore.QRect(15, 195, 145, 22))
        self.templateVerChbx.setFont(self.newfont)
        self.templateVerChbx.setObjectName("template ver")
        self.templateVerChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.templateVerChbx.setText("Template Version : ")
        
        self.templateNameChbx = QtGui.QCheckBox(self.generalTab)
        self.templateNameChbx.setGeometry(QtCore.QRect(15, 235, 145, 22))
        self.templateNameChbx.setFont(self.newfont)
        self.templateNameChbx.setObjectName("template name")
        self.templateNameChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.templateNameChbx.setText("Template Name : ")
        
        self.serialNoChbx = QtGui.QCheckBox(self.generalTab)
        self.serialNoChbx.setGeometry(QtCore.QRect(225, 25, 145, 22))
        self.serialNoChbx.setFont(self.newfont)
        self.serialNoChbx.setObjectName("serial number")
        self.serialNoChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.serialNoChbx.setText("Serial Number : ")
         
        self.flashbytesChbx = QtGui.QCheckBox(self.generalTab)
        self.flashbytesChbx.setGeometry(QtCore.QRect(225, 65, 145, 22))
        self.flashbytesChbx.setFont(self.newfont)
        self.flashbytesChbx.setObjectName("flash free")
        self.flashbytesChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.flashbytesChbx.setText("Flash free bytes : ")
        
        self.lastConfigChbx = QtGui.QCheckBox(self.generalTab)
        self.lastConfigChbx.setGeometry(QtCore.QRect(210, 110, 162, 25))
        self.lastConfigChbx.setFont(self.newfont)
        self.lastConfigChbx.setObjectName("Last config change")
        self.lastConfigChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.lastConfigChbx.setText("Last Config change : ")
        
        self.AsprChbx = QtGui.QCheckBox(self.generalTab)
        self.AsprChbx.setGeometry(QtCore.QRect(210, 150, 162, 25))
        self.AsprChbx.setFont(self.newfont)
        self.AsprChbx.setObjectName("ASPR")
        self.AsprChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.AsprChbx.setText("ASPR ? Yes/No : ")
        
        self.exceptionChbx = QtGui.QCheckBox(self.generalTab)
        self.exceptionChbx.setGeometry(QtCore.QRect(185, 190, 188, 30))
        self.exceptionChbx.setFont(self.newfont)
        self.exceptionChbx.setObjectName("ASPR")
        self.exceptionChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.exceptionChbx.setText("Exception Info, Yes/No : ")
          
#         self.excel_opt_error_label =  QtGui.QLabel(self.gui) # error label
#         self.excel_opt_error_label.setText("Please select appropriate options for data extraction.")
#         self.excel_opt_error_label.setFont(QtGui.QFont("Verdana", 9, QtGui.QFont.Normal))
#         self.excel_opt_error_label.setStyleSheet("color: red")
#         self.excel_opt_error_label.hide()
        #self.radio_option_layout_lb_h.addWidget(self.excel_opt_error_label)
    
        
#==================================  audit tab below

        
        self.auditTab = QtGui.QWidget()
        self.auditTab.setObjectName("audit")
        self.userOptionextract.addTab(self.auditTab,"Audit") 
        
        
        
        self.partNumChbx = QtGui.QCheckBox(self.auditTab)
        self.partNumChbx.setGeometry(QtCore.QRect(15, 25, 145, 22))
        self.partNumChbx.setFont(self.newfont)
        self.partNumChbx.setObjectName("Part number")
        self.partNumChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.partNumChbx.setText("Part Number : ")
        
        self.partNameChbx = QtGui.QCheckBox(self.auditTab)
        self.partNameChbx.setGeometry(QtCore.QRect(15, 65, 145, 22))
        self.partNameChbx.setFont(self.newfont)
        self.partNameChbx.setObjectName("Part name")
        self.partNameChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.partNameChbx.setText("Part Name : ")
        
        self.auditSerialChbx = QtGui.QCheckBox(self.auditTab)
        self.auditSerialChbx.setGeometry(QtCore.QRect(15, 105, 145, 22))
        self.auditSerialChbx.setFont(self.newfont)
        self.auditSerialChbx.setObjectName("serial")
        self.auditSerialChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.auditSerialChbx.setText("Serial Number : ")
        
        self.auditDescrChbx = QtGui.QCheckBox(self.auditTab)
        self.auditDescrChbx.setGeometry(QtCore.QRect(15, 145, 145, 22))
        self.auditDescrChbx.setFont(self.newfont)
        self.auditDescrChbx.setObjectName("description")
        self.auditDescrChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.auditDescrChbx.setText("Description : ")
        #============================== Network tab below
        
        self.networkTab = QtGui.QWidget()
        self.networkTab.setObjectName("network")
        self.userOptionextract.addTab(self.networkTab,"Network") 
        
        
        self.mgmtIPchbx = QtGui.QCheckBox(self.networkTab)
        self.mgmtIPchbx.setGeometry(QtCore.QRect(15, 25, 145, 22))
        self.mgmtIPchbx.setFont(QtGui.QFont("Verdana", 8, QtGui.QFont.Normal))
        self.mgmtIPchbx.setObjectName("MGMT IP")
        self.mgmtIPchbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.mgmtIPchbx.setText("Management IP : ")
        
        self.mgmtVlanchbx = QtGui.QCheckBox(self.networkTab)
        self.mgmtVlanchbx.setGeometry(QtCore.QRect(15, 65, 145, 22))
        self.mgmtVlanchbx.setFont(QtGui.QFont("Verdana", 7, QtGui.QFont.Normal))
        self.mgmtVlanchbx.setObjectName("MGMT VLAN")
        self.mgmtVlanchbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.mgmtVlanchbx.setText("MGMT VLAN : ")
        
        self.dataVlanchbx = QtGui.QCheckBox(self.networkTab)
        self.dataVlanchbx.setGeometry(QtCore.QRect(15, 105, 145, 22))
        self.dataVlanchbx.setFont(QtGui.QFont("Verdana", 7, QtGui.QFont.Normal))
        self.dataVlanchbx.setObjectName("DATA VLAN")
        self.dataVlanchbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.dataVlanchbx.setText("DATA VLAN : ")
        
        self.voiceVlanchbx = QtGui.QCheckBox(self.networkTab)
        self.voiceVlanchbx.setGeometry(QtCore.QRect(15, 145, 145, 22))
        self.voiceVlanchbx.setFont(QtGui.QFont("Verdana", 7, QtGui.QFont.Normal))
        self.voiceVlanchbx.setObjectName("VOICE VLAN")
        self.voiceVlanchbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.voiceVlanchbx.setText("VOICE VLAN : ")
        
        self.wirelessVlanchbx = QtGui.QCheckBox(self.networkTab)
        self.wirelessVlanchbx.setGeometry(QtCore.QRect(15, 185, 145, 22))
        self.wirelessVlanchbx.setFont(QtGui.QFont("Verdana", 7, QtGui.QFont.Normal))
        self.wirelessVlanchbx.setObjectName("WIRELESS VLAN")
        self.wirelessVlanchbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.wirelessVlanchbx.setText("WIRELESS VLAN : ")
        
        self.othervlanChbx = QtGui.QCheckBox(self.networkTab)
        self.othervlanChbx.setGeometry(QtCore.QRect(15, 225, 145, 22))
        self.othervlanChbx.setFont(self.newfont)
        self.othervlanChbx.setObjectName("Other VLAN")
        self.othervlanChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.othervlanChbx.setText("Other VLANs : ")
        
        self.trunkChbx = QtGui.QCheckBox(self.networkTab)
        self.trunkChbx.setGeometry(QtCore.QRect(15, 265, 145, 22))
        self.trunkChbx.setFont(self.newfont)
        self.trunkChbx.setObjectName("Trunk links")
        self.trunkChbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.trunkChbx.setText("Trunk Ports : ")
        
        
        self.gatewayIPchbx = QtGui.QCheckBox(self.networkTab)
        self.gatewayIPchbx.setGeometry(QtCore.QRect(225, 25, 145, 22))
        self.gatewayIPchbx.setFont(self.newfont)
        self.gatewayIPchbx.setObjectName("Gateway IP")
        self.gatewayIPchbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.gatewayIPchbx.setText("Gateway IP : ")
        
        self.parentDevicechbx = QtGui.QCheckBox(self.networkTab)
        self.parentDevicechbx.setGeometry(QtCore.QRect(225, 65, 145, 22))
        self.parentDevicechbx.setFont(self.newfont)
        self.parentDevicechbx.setObjectName("Parent Device")
        self.parentDevicechbx.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.parentDevicechbx.setText("Parent Device : ")

       #============================== Search tab below # search option         
        self.searchTab = QtGui.QWidget()
        self.searchTab.setObjectName("search")
        self.userOptionextract.addTab(self.searchTab,"Search") 
        
        self.search_pat_label =  QtGui.QLabel(self.searchTab)
        self.search_pat_label.setText("Command pattern :")
        self.search_pat_label.setFont(QtGui.QFont("Verdana", 8, QtGui.QFont.Normal))
        self.search_pat_label.setToolTip("Enter commands in input box provided below for searching.")
        self.search_pat_label.setGeometry(QtCore.QRect(15, 25, 120, 21))
        
        self.search_command_box = QtGui.QTextEdit(self.searchTab)
        self.search_command_box.setGeometry(QtCore.QRect(15, 65, 345, 27))
        self.search_command_box.setFont(self.newfont)
        self.search_command_box.setObjectName("Search")
        self.search_command_box.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.search_command_box.setToolTip("Enter command pattern to extract in excel sheet! Please enter commands seperated by commas if there are multiple commands to search..")
       
    
        self.userOptionextract.hide()
        
        self.excel_disp_flag = False
        
    def display_excel_portion(self):
        
        self.left_common.last_parent.credentials_groupbox.show()
        self.left_common.last_parent.IP_groupBox.show()
        self.left_common.last_parent.Commands_groupBox.show()
        self.left_common.last_parent.results_groupBox.show()
        self.left_common.show_left_common()
        self.userOptionextract.show()
        self.excel_disp_flag = True
        
        self.left_common.go_button.show()
        self.left_common.go_button.setText("Extract")
        
    
                