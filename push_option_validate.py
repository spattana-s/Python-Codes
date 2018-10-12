'''
Created on Jul 11, 2018

@author: rg012f
'''
from PySide import QtGui

class validate_push_opt:

    def __init__(self,last_parent,common_model,model_push):
        
        self.last_parent = last_parent
        self.common_model = common_model
        self.model_push = model_push
    
    def kick_push_view_validations(self):
        self.ip_box_cnt = self.last_parent.base_left.ip_add_box.toPlainText()
        self.command_box_cnt = self.last_parent.base_left.commands_box.toPlainText()
#         self.cr_number = self.last_parent.base_left.cr_box.toPlainText()
        
        if self.common_model.usr_name_given_flag == "Green" and self.common_model.psw_given_flag== "Green" and self.common_model.cr_given_flag == "Green" :
            print("push_option_validate 39")
            if self.common_model.ip_address_input_flag == "Green" and self.common_model.commands_input_flag == "Green" :
                self.model_push.push_proceed_flag = "Green"
                print("push_option_validate 45")
            else:
                self.model_push.push_proceed_flag = "Red"
        else:
            self.model_push.push_proceed_flag = "Red"
            self.last_parent.base_left.msgBox.critical(self.last_parent.gui,'Credentials Missing',"Username or Password Missing", QtGui.QMessageBox.Abort)    
                
#             if len(self.ip_box_cnt) >0 : # below block is for updating ip address box content in model class
#                 self.common_model.ipadd_box_filled = True  # resetting ip address box filled flag to true
#                 self.model_push.push_proceed_flag = 'Green'
#                 self.common_model.ipadd_box_content = self.last_parent.base_left.ip_add_box.toPlainText()
#                 print("push_option_validate line 59")
#                 
#                     
#             elif len(self.ip_box_cnt) <= 0:
#                 self.common_model.ipadd_box_filled = False  # resetting ip address box filled flag to true
#                 self.common_model.ipadd_box_content = ''
#                 print("push_option_validate 65")
#                 
#                 if self.common_model.ipaddress_file_selected == False:
#                     self.model_push.push_proceed_flag='Red'
#                     self.common_model.proceed_signal = "Red"
#                     self.last_parent.base_left.msgBox.critical(self.last_parent.gui,'Input Error!',"Please select correct file type (.txt) which contains valid IP addresses...!", QtGui.QMessageBox.Abort)
#                     self.last_parent.base_left.ipadd_file_error_label.setText("Select IP address file or enter IP details in the box provided ..!")
#                     self.last_parent.base_left.ipadd_file_error_label.setStyleSheet("color: red")
#                     self.last_parent.base_left.ipadd_file_error_label.show()
#                     print("push_option_validate 74")
#                 else:
#                     self.model_push.push_proceed_flag='Green'
#                     self.common_model.proceed_signal = "Green" 
#                     print("kick_push_view_validations line77")                
                    
                
        