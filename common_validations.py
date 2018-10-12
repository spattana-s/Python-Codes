'''
Created on 15 june, 2018

@author: sp977u@att.com  (Satish Palnati)

This class is for validating common options for all views and update the model class

Note :  we have to remove the dependency on error label for showing filename label.  Create a new label for that.

'''
# from PySide import QtGui

class validate_common_option:

    def __init__(self,last_parent,common_model):
        
        self.last_parent = last_parent
        self.common_model = common_model
    
    def kick_common_validations(self):
        self.ip_box_cnt = self.common_model.ipadd_box_content[:]
        self.commands_box_cnt = self.common_model.commands_box_content[:]
        
        self.common_model.output_path= self.last_parent.output_folder
        
        
        if len(self.last_parent.base_left.UsernameBox.text()) >0 :
            self.common_model.usr_name_given_flag = "Green"
            self.common_model.user_name = self.last_parent.base_left.UsernameBox.text()      #Repetaed command, removed toplaintext
            
            if self.last_parent.base_left.saveUseranme.isChecked():
                try:
                    f = open('Username.txt','w')
                    f.write(self.common_model.user_name)
                except Exception as ex:
                    print(ex)
                    
            else:
                try:
                    f = open('Username.txt','w')
                    f.clear()
                    
                except Exception as ex:
                    print(ex)
                    
            self.last_parent.base_left.username_error_label.hide()
            print("kick_common_validations line32")
        elif self.common_model.ping_only_selected == True:
            self.common_model.usr_name_given_flag = "Red"
            self.last_parent.base_left.username_error_label.hide()
            self.common_model.user_name = "NF"
            print("kick_common_validations line37")
        else:
            self.common_model.usr_name_given_flag = "Red"
            self.last_parent.base_left.username_error_label.show()
            self.common_model.user_name = "NF"
            print("kick_common_validations line42")
            
        if len(self.last_parent.base_left.PassBox.text()) >0:
            self.common_model.psw_given_flag = "Green"
            self.common_model.psw = self.last_parent.base_left.PassBox.text()
            self.last_parent.base_left.pass_error_label.hide()
            print("kick_common_validations line48")
        elif self.common_model.ping_only_selected == True:
            self.common_model.usr_name_given_flag = "Red"
            self.last_parent.base_left.pass_error_label.hide()
            self.common_model.user_name = "NF"
            print("kick_common_validations line53")
        else:
            self.last_parent.base_left.pass_error_label.show()
            self.common_model.psw_given_flag = "Red"
            self.common_model.psw = ''
            print("kick_common_validations line58")
            
            
        if self.last_parent.push_radio_option.isChecked():
            if len(self.last_parent.base_left.cr_box.text()) > 0 :
                self.common_model.cr_given_flag = "Green"
                self.common_model.cr_number = self.last_parent.base_left.cr_box.text()
                self.last_parent.base_left.cr_error_label.hide()
                print("kick_common_validations line83")
            else:
                self.common_model.cr_given_flag = "Red"
                self.common_model.cr_number = 'NF'
                self.last_parent.base_left.cr_error_label.show()
                print("kick_common_validations line87")
            
######ip_address validations##################

        if ( len(self.common_model.ipaddress_file) <= 0 or self.common_model.ipaddress_file == "NF" ) and len(self.ip_box_cnt) <= 0 :   
            self.last_parent.base_left.ipadd_file_error_label.show()
            self.last_parent.base_left.ipadd_file_error_label.setStyleSheet("color: red")
            self.last_parent.base_left.ipadd_file_name_label.hide()
            self.common_model.ipaddress_file_selected = False
            self.common_model.ipadd_box_filled = False
            self.common_model.ip_address_input_flag = "Red"
            print("kick_common_validations line69")
            
        else:
            if len(self.ip_box_cnt) <= 0 :
                
                if ".txt" in self.common_model.ipaddress_file.lower() and self.common_model.valid_ip_flag == "Green":
                    self.last_parent.base_left.ipadd_file_name_label.show()
                    self.last_parent.base_left.ipadd_file_name_label.setStyleSheet("color: green")
                    self.common_model.ip_address_input_flag = "Green"
                    self.common_model.ipaddress_file_selected = True
                    print("kick_common_validations line63")
                    
                else :
                    self.last_parent.base_left.ipadd_file_error_label.show()
                    self.last_parent.base_left.ipadd_file_name_label.show()
                    self.last_parent.base_left.ipadd_file_error_label.setStyleSheet("color: red")
                    self.last_parent.base_left.ipadd_file_name_label.setStyleSheet("color: red")
                    self.common_model.ip_address_input_flag = "Red"
                    print("kick_common_validations line73")
                    
            else : 
                self.common_model.ipadd_box_filled = True
                
                if ".txt" in self.common_model.ipaddress_file.lower() and self.common_model.valid_ip_flag == "Green":
                    self.last_parent.base_left.ipadd_file_name_label.show()
                    self.last_parent.base_left.ipadd_file_name_label.setStyleSheet("color: green")
                    self.last_parent.base_left.ipadd_file_error_label.hide()
                    self.common_model.ip_address_input_flag = "Green"
                    self.common_model.ipaddress_file_selected = True
                    print("kick_common_validations line84")
                    
                elif len(self.common_model.ipaddress_file) > 0 and self.common_model.ipaddress_file != "NF" and self.common_model.valid_ip_flag == "Green": 
                    self.last_parent.base_left.ipadd_file_name_label.show()
                    self.last_parent.base_left.ipadd_file_name_label.setStyleSheet("color: red")
                    self.common_model.ip_address_input_flag = "Green"
                    self.common_model.ipaddress_file_selected = False
#                     self.last_parent.base_left.ipadd_file_error_label.show()
                    self.last_parent.base_left.ipadd_file_error_label.setStyleSheet("color: red")
                    print("kick_common_validations line92")
#                  and self.common_model.valid_ip_flag == "Green"
                elif self.common_model.ipaddress_file_selected == False and self.common_model.valid_ip_flag == "Green":
                    self.last_parent.base_left.ipadd_file_error_label.hide()
                    self.common_model.ip_address_input_flag = "Green"
                    print("kick_common_validations line140")
                    
                
######## Command input file and box Validations ############    
        
        if self.last_parent.base_left.default_commands_chbx.isChecked():
            self.common_model.default_commands_set = True
        else:
            self.common_model.default_commands_set = False
            
        if self.last_parent.base_left.commands_file_radio.isChecked():
            
            if len(self.common_model.command_file) >0 and ".txt" in self.common_model.command_file :
                self.common_model.command_file_selected = True
                self.common_model.commands_input_flag = "Green"
                
            elif self.common_model.command_file != "NF":
                self.common_model.command_file_selected = True
                self.common_model.commands_input_flag = "Red"
                
            else:
                self.common_model.command_file_selected = False
                self.common_model.commands_input_flag = "Red"
            
        elif self.last_parent.base_left.commands_custom_radio.isChecked() : 
            if len(self.common_model.commands_box_content) > 0:
                self.common_model.commands_box_filled = True
                self.common_model.commands_input_flag = "Green"
                print("common validaions 159")
            else:
                self.common_model.commands_box_filled = False
                self.common_model.commands_input_flag = "Red"
                print("common validaions 163")
                
        elif self.last_parent.base_left.none_radio.isChecked():
            self.common_model.commands_box_filled = False
            self.common_model.command_file_selected = False
            if self.common_model.default_commands_set == True:
                self.common_model.commands_input_flag = "Green"
            else:
                self.common_model.commands_input_flag = "Red"
                print("common validaions 169")
