'''
Created on 15 june, 2018

@author: sp977u@att.com  (Satish Palnati)

This class is for validating extract view and update the model class

'''
from PySide import QtGui


class validate_extract_option:

    def __init__(self,last_parent,common_model,model_extract):
        
        self.last_parent = last_parent
        self.common_model = common_model
        self.model_extract = model_extract
    
    def kick_extract_view_validations(self):
        
        
        if self.last_parent.excel_view.ipaddChbx.isChecked():
            self.model_extract.extract_list.append("IP Address")
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.hostNameChbx.isChecked():
            self.model_extract.extract_list.append('Hostname')
            self.model_extract.total_extract_count += 1
        
        if self.last_parent.excel_view.modelChbx.isChecked():
            self.model_extract.extract_list.append('Model')
            self.model_extract.total_extract_count += 1
        
        if self.last_parent.excel_view.osversionChbx.isChecked():
            self.model_extract.extract_list.append('OS version')
            self.model_extract.total_extract_count += 1
        
        if self.last_parent.excel_view.templateVerChbx.isChecked():
            self.model_extract.extract_list.append('Template Version')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.templateNameChbx.isChecked():
            self.model_extract.extract_list.append('Template Name')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.serialNoChbx.isChecked():
            self.model_extract.extract_list.append("Serial Number")
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.flashbytesChbx.isChecked():
            self.model_extract.extract_list.append('Flash free bytes')
            self.model_extract.total_extract_count += 1
        
        if self.last_parent.excel_view.lastConfigChbx.isChecked():
            self.model_extract.extract_list.append('Last Config change')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.AsprChbx.isChecked():
            self.model_extract.extract_list.append('ASPR ? Yes/No')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.exceptionChbx.isChecked():
            self.model_extract.extract_list.append('Exception Info, Yes/No')
            self.model_extract.total_extract_count += 1
            
#==================================  check box for audit tab below

        if self.last_parent.excel_view.partNumChbx.isChecked():
            self.model_extract.extract_list.append('Part Number')
            self.model_extract.total_extract_count += 1
        
        if self.last_parent.excel_view.partNameChbx.isChecked():
            self.model_extract.extract_list.append('Part Name')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.auditSerialChbx.isChecked():
            self.model_extract.extract_list.append('Serial Number')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.auditDescrChbx.isChecked():
            self.model_extract.extract_list.append('Description')
            self.model_extract.total_extract_count += 1
            
#==================================  check box for network tab below
        
        if self.last_parent.excel_view.mgmtIPchbx.isChecked():
            self.model_extract.extract_list.append('Management IP')
            self.model_extract.total_extract_count += 1
        
        if self.last_parent.excel_view.mgmtVlanchbx.isChecked():
            self.model_extract.extract_list.append('MGMT VLAN')
            self.model_extract.total_extract_count += 1
    
        if self.last_parent.excel_view.dataVlanchbx.isChecked():
            self.model_extract.extract_list.append('DATA VLAN')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.voiceVlanchbx.isChecked():
            self.model_extract.extract_list.append('VOICE VLAN')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.wirelessVlanchbx.isChecked():
            self.model_extract.extract_list.append("WIRELESS VLAN")
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.othervlanChbx.isChecked():
            self.model_extract.extract_list.append('Other VLANs')
            self.model_extract.total_extract_count += 1
        
        if self.last_parent.excel_view.trunkChbx.isChecked():
            self.model_extract.extract_list.append('Trunk Ports')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.gatewayIPchbx.isChecked():
            self.model_extract.extract_list.append('Gateway IP')
            self.model_extract.total_extract_count += 1
            
        if self.last_parent.excel_view.parentDevicechbx.isChecked():
            self.model_extract.extract_list.append('Parent Device')
            self.model_extract.total_extract_count += 1
              
#==================================  check box for search tab below
            
        if len(self.last_parent.excel_view.search_command_box.toPlainText())>0:
            self.model_extract.extract_list.append('Search Pattern')
            self.model_extract.total_extract_count += 1
    