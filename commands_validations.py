'''
Created on 26 june, 2018

@author: sp977u@att.com  (Satish Palnati)

This class is written for validating Commands info from both .txt file and  from input box on GUI . 
We consider either box or File content only based on check box selection by user.
'''
from PySide import QtGui

class commandsLoadingValidate:

    def __init__(self,last_parent):
        
        self.last_parent = last_parent
        self.commands_file = 'NF'
        self.commands_box_content = ''
   
    def load_commands(self,commands_file,commands_box_content):
        self.commands_file = commands_file
        self.commands_box_content = commands_box_content
        
        self.last_parent.validations.common_model.final_commands_list.clear()
        self.last_parent.base_left.cmds_error_label.hide()
        
        if self.last_parent.validations.model_get.get_proceed_flag == "Green":
            if self.last_parent.validations.common_model.usr_name_given_flag == "Green" and self.last_parent.validations.common_model.psw_given_flag == "Green":
                if self.last_parent.validations.common_model.ip_address_input_flag == 'Green' or self.last_parent.validations.common_model.ipadd_box_filled == True : 
                    print('Commands_Validations 34')
# check for default option           
                    if self.last_parent.validations.common_model.default_commands_set == True:
                        self.last_parent.validations.model_get.get_proceed_flag = 'Green'
                        
                    else: 
                        self.last_parent.validations.common_model.final_commands_list.clear()
                        pass
# check for custom radio
                    if self.last_parent.base_left.commands_custom_radio.isChecked():
                        if self.last_parent.validations.common_model.commands_box_filled == True:
                            self.last_parent.validations.common_model.final_commands_list += (self.commands_box_content.replace("\n", ',').replace(';', ',').split(','))
                            self.last_parent.validations.model_get.get_proceed_flag = 'Green'
                            print('Commands_Validations 40')
        
                        else:
                            self.last_parent.validations.model_get.get_proceed_flag = 'Red'
                            self.last_parent.msgBox.critical(self.last_parent.gui,'Command Box Empty..!','No Commands have been entered in the text box..!!', QtGui.QMessageBox.Ok)
                            self.last_parent.base_left.cmds_error_label.setStyleSheet("color: red;")
                            self.last_parent.base_left.cmds_error_label.setText("Enter Command details in input box provided ..!")
                            self.last_parent.base_left.cmds_error_label.show()
#check for file                 
                    if self.last_parent.base_left.commands_file_radio.isChecked():
                        if self.last_parent.validations.common_model.command_file_selected == True:
                            self.last_parent.validations.common_model.command_file_list.clear() # cleaning the file for reuse
                            print('Commands_Validations 43')
                            try :
                                commands_file_handler = open(self.commands_file,'r')
                                print('Commands_Validations 43')
                                lines = commands_file_handler.readlines()
                                
                                print(len(lines))
                                
                                for item in lines:
                                    item=item.replace('\n','').strip()
                                    if len(item)>0:
                                        self.last_parent.validations.common_model.command_file_list.append(item)
                                    else:
                                        continue
                                    
                                print(len(self.last_parent.validations.common_model.command_file_list))
                                
                                if len(self.last_parent.validations.common_model.command_file_list) > 0:
                                    self.last_parent.validations.model_get.get_proceed_flag = 'Green'
                                    # final list to be passed for config_engine
                                    self.last_parent.validations.common_model.final_commands_list += (self.last_parent.validations.common_model.command_file_list)
                                    print('Commands_Validations 70')
                                else:
                                    self.last_parent.msgBox.critical(self.last_parent.gui,'File Empty..!','Empty File or No Commands have been entered in the text box..!!', QtGui.QMessageBox.Ok)
                                    self.last_parent.validations.model_get.get_proceed_flag = 'Red'
                            
                            except FileNotFoundError:
                                self.last_parent.msgBox.critical(self.last_parent.gui,'No File Selected','Empty File or No Commands have been entered in the text box..!!', QtGui.QMessageBox.Ok)
                                self.last_parent.validations.model_get.get_proceed_flag = 'Red'
                            except Exception as ex: 
                                
                                print('Commands_Validations 67')
                                print("error msg : " ,ex)
                        else:
                            self.last_parent.msgBox.critical(self.last_parent.gui,'No File Selected..!','No Commands file has been given..!!', QtGui.QMessageBox.Ok)
                            self.last_parent.validations.model_get.get_proceed_flag = 'Red'
                            self.last_parent.base_left.cmds_error_label.setStyleSheet("color: red;")
                            self.last_parent.base_left.cmds_error_label.setText("Please Enter a Commands File..!!")
                            self.last_parent.base_left.cmds_error_label.show()
# check for none
                
                    if self.last_parent.base_left.none_radio.isChecked():
                        if self.last_parent.validations.common_model.default_commands_set == True:
                            self.last_parent.validations.model_get.get_proceed_flag = 'Green'
                            pass
                        else:
                            self.last_parent.msgBox.critical(self.last_parent.gui,'No option selected','Please give Command Inputs..!!', QtGui.QMessageBox.Ok)
                            self.last_parent.validations.model_get.get_proceed_flag = 'Red'
                        print("Commands_Validations 89 ")
        
                else:
                    self.last_parent.msgBox.critical(self.last_parent.gui,'IP File Missing',"Please Upload IP File or enter IPs in the Text Box to run Commands", QtGui.QMessageBox.Ok)
                    self.last_parent.validations.model_get.get_proceed_flag = 'Red'
                    print('Commands_Validations 94')
            else:
                self.last_parent.msgBox.critical(self.last_parent.gui,'Credentials Missing',"Username or Password Missing", QtGui.QMessageBox.Ok)
                self.last_parent.validations.model_get.get_proceed_flag = 'Red'
                print('Commands_Validations 108')
        
        else:
            self.last_parent.validations.model_get.get_proceed_flag == "Red"
        
        