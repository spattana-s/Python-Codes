'''
Created on 15 june, 2018

@author: sp977u@att.com  (Satish Palnati)

This class is for validating get view and update the model class

Pleases take care of logging part

'''
from PySide import QtGui

class validate_get_opt:

    def __init__(self,last_parent,common_model,model_get):
        
        self.last_parent = last_parent
        self.common_model = common_model
        self.model_get = model_get
    
    def kick_get_view_validations(self):
        self.ip_box_cnt = self.last_parent.base_left.ip_add_box.toPlainText()
        self.command_box_cnt = self.last_parent.base_left.commands_box.toPlainText()
        
        if self.last_parent.base_left.get_ping_logs_chbx.isChecked():
            self.last_parent.base_left.get_conf_logs_chbx.setChecked(False)
            self.model_get.get_config_logs_selected = False
            self.model_get.ping_logs_only = True
            print("get_option_validate 31")
            
        elif not self.last_parent.base_left.get_ping_logs_chbx.isChecked() and self.last_parent.base_left.get_conf_logs_chbx.isChecked():
            self.last_parent.base_left.get_ping_logs_chbx.setChecked(False)
            self.model_get.get_config_logs_selected = True
            print("get_option_validate 36")
            if self.common_model.usr_name_given_flag == "Green" and self.common_model.psw_given_flag== "Green" :
                print("get_option_validate 39")
                if self.common_model.ip_address_input_flag == "Green" and self.common_model.commands_input_flag == "Green" :
                    self.model_get.get_proceed_flag = "Green"
                    print("get_option_validate 45")
                else:
                    self.model_get.get_proceed_flag = "Red"
            else:
                self.model_get.get_proceed_flag = "Red"
                
        if self.last_parent.base_left.get_ping_logs_chbx.isChecked() or self.last_parent.base_left.get_conf_logs_chbx.isChecked():
            print("get_option_validate 51")
            if (self.last_parent.base_left.get_ping_logs_chbx.isChecked() or self.last_parent.base_left.get_conf_logs_chbx.isChecked()) and ( self.common_model.ipaddress_file != "NF"  or  len(self.ip_box_cnt) > 0) :
                print(self.common_model.ipaddress_file)
                print("get_option_validate 54")
                if len(self.ip_box_cnt) >0 : # below block is for updating ip address box content in model class
                    self.common_model.ipadd_box_filled = True  # resetting ip address box filled flag to true
                    self.model_get.get_proceed_flag = 'Green'
                    self.common_model.ipadd_box_content = self.last_parent.base_left.ip_add_box.toPlainText()
                    print("get_option_validate line 59")
                    
                    
                elif len(self.ip_box_cnt) <= 0:
                    self.common_model.ipadd_box_filled = False  # resetting ip address box filled flag to true
                    self.common_model.ipadd_box_content = ''
                    print("get_option_validate 65")
                    
                    if self.common_model.ipaddress_file_selected == False:
                        self.model_get.get_proceed_flag='Red'
                        self.common_model.proceed_signal = "Red"
                        self.last_parent.base_left.msgBox.critical(self.last_parent.gui,'Input Error!',"Please select correct file type (.txt) which contains valid IP addresses...!", QtGui.QMessageBox.Abort)
                        self.last_parent.base_left.ipadd_file_error_label.setText("Select IP address file or enter IP details in the box provided ..!")
                        self.last_parent.base_left.ipadd_file_error_label.setStyleSheet("color: red")
                        self.last_parent.base_left.ipadd_file_error_label.show()
                        print("get_option_validate 74")
                    else:
                        self.model_get.get_proceed_flag='Green'
                        self.common_model.proceed_signal = "Green" 
                        print("kick_get_view_validations line77")   
            else:
                print("file selected :  ",self.common_model.ipaddress_file)
                print("get_option_validate 80")
                self.last_parent.base_left.ipadd_file_error_label.setText("Select IP address file or enter IP details in the box provided ..!")
                self.last_parent.base_left.ipadd_file_error_label.setStyleSheet("color: red")
                self.last_parent.base_left.ipadd_file_error_label.show()
                self.model_get.get_proceed_flag='Red'
                self.common_model.proceed_signal = "Red"
                
        if self.last_parent.get_radio_option.isChecked() and ( not self.last_parent.base_left.get_ping_logs_chbx.isChecked() and not self.last_parent.base_left.get_conf_logs_chbx.isChecked()) :
            self.last_parent.base_left.msgBox.critical(self.last_parent.gui,'Option Error!',"Please select at  least one get Option to proceed...!", QtGui.QMessageBox.Abort)
            self.model_get.get_proceed_flag= 'Red'
            self.common_model.proceed_signal = "Red"
