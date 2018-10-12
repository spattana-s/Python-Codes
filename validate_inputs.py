'''
Created on 1 june, 2018

@author: sp977u@att.com  (Satish Palnati)

'''
from PySide import QtGui
from models import common_model
from models.get_model import get_option_model
from models.push_model import push_option_model
from models.extract_model import extract_option_model
from models.compare_model import compare_option_model
from validations.get_option_validate import validate_get_opt
from validations.push_option_validate import validate_push_opt
from validations.common_validations import validate_common_option
from validations.extract_option_validate import validate_extract_option
from validations.compare_option_validate import validate_compare_opt
from validations.ipaddress_validations import ipAddressValidate
from Speed_Engine.start_ping_engine import PingEngine
from Speed_Engine.config_engine import ConfigEngine
from Speed_Engine.push_engine import PushEngine
from Speed_Engine.comapre_engine import ComapreEngine
from validations.commands_validations import commandsLoadingValidate
from views.common.compare_view import compare_op_results

class validate_controls:

    def __init__(self,ui_inst):
        
        self.ui_inst = ui_inst    # ui_inst is last_parent is other classes,  it is self object from ui_parent_view module
        self.excel_disp_flag = False
        self.common_model = common_model.common_options_model()
        self.model_get =  get_option_model() # get model for mapping values for this option
        self.model_push = push_option_model()
        self.model_extract = extract_option_model() # excel extraction specific model for model updation
        self.model_compare = compare_option_model()
        
        self.common_validate = validate_common_option(ui_inst,self.common_model)
        self.get_validate = validate_get_opt(ui_inst,self.common_model,self.model_get)  # get validations instance creation if user selected get radio button
        self.push_validate = validate_push_opt(ui_inst,self.common_model,self.model_push)
        self.extract_validate = validate_extract_option(ui_inst,self.common_model,self.model_extract)
        self.compare_validate = validate_compare_opt(ui_inst,self.common_model,self.model_compare)
        
        self.ip_file_validate = ipAddressValidate(ui_inst) # to check valid ip addresses from file and input box
        self.commands_validate = commandsLoadingValidate(ui_inst)
        self.ping_engine_object = PingEngine(self.common_model,self.ui_inst ) # instance creation of Engine class
        self.config_engine_object = ConfigEngine(self.common_model,self.ui_inst)
        self.push_engine_object = PushEngine(self.common_model,self.ui_inst)
        
        self.compare_engine_object = ComapreEngine(self.common_model,self.ui_inst)
        self.compare_view_object = compare_op_results(self.ui_inst)
        
        
        
    def validate_user_inputs(self,):
        
        
        final_result = "FAIL"
        self.ip_box_cnt = self.ui_inst.base_left.ip_add_box.toPlainText()
        self.commands_box_cnt = self.ui_inst.base_left.commands_box.toPlainText()
        
        self.reset_data_values()  # for resetting values to defaults before validations
        
        self.common_model.output_path = self.ui_inst.output_folder  # UPDAING output folder path to model class which user selects 
        # IP VALIDATE here call to use valid ip flag further for ip_input_flag green or red
        # Updating ip_box commands box in common model
        self.common_model.ipadd_box_content= self.ui_inst.base_left.ip_add_box.toPlainText()
        self.common_model.commands_box_content = self.ui_inst.base_left.commands_box.toPlainText()
        
        self.ip_file_validate.check_valid_ip_addresses(self.common_model.ipaddress_file,self.common_model.ipadd_box_content) # common ip address validations for all radio options
        self.common_validate.kick_common_validations()# doing common control validations and updating common model class
        
# for Get    
        if self.ui_inst.get_radio_option.isChecked():
            self.get_validate.kick_get_view_validations()  # calling method to validate data and update model for get option
            #loading commands validation            
            if self.model_get.get_config_logs_selected == True:
                self.commands_validate.load_commands(self.common_model.command_file, self.common_model.commands_box_content)
                
            if self.model_get.get_proceed_flag == "Green" :
                if self.common_model.ping_only_selected == True:
                    self.hide_right_common()
                    self.ui_inst.base_left.go_button.setDisabled(True)  # will be re-enabled in engine 
                    self.ping_engine_object.start_ping_engine()
                
                elif self.model_get.get_config_logs_selected == True:
                    self.hide_right_common()
                    self.ui_inst.base_left.go_button.setDisabled(True)  # will be re-enabled in engine
                    self.config_engine_object.start_config_engine()
                    print("I have reached get configurations op")
                
# for Push
        if self.ui_inst.push_radio_option.isChecked():
            self.push_validate.kick_push_view_validations()  # calling method to validate data and update model for get option
            print("Push ip flag", self.common_model.ip_address_input_flag)
            print("push commands flag",self.common_model.commands_input_flag)
            print("line 86 Validate inputs ",self.model_push.push_proceed_flag)
            self.commands_validate.load_commands(self.common_model.command_file, self.common_model.commands_box_content)
            print("line 88 Validate inputs ",self.model_push.push_proceed_flag) 
            
            if self.model_push.push_proceed_flag == "Green" :
                print("line 62 Validate inputs ",self.model_push.push_proceed_flag)
                
                self.hide_right_common()
                self.ui_inst.base_left.go_button.setDisabled(True)  # will be re-enabled in engine 
                self.push_engine_object.start_push_engine()  # start push engine
                print("I have reached push op")

            
            
# for Extract.  User has to select atleast one option other than IP address .            
        if self.ui_inst.extract_radio_option.isChecked():
            self.extract_validate.kick_extract_view_validations()
            print("Ext list : ",self.model_extract.extract_list)
            print("Total cout : ",self.model_extract.total_extract_count)  

# for Compare
        if self.ui_inst.compare_radio_option.isChecked():
            self.compare_validate.kick_compare_view_validations()
            self.hide_right_common()
            self.compare_engine_object.start_compare_engine()



  
    def reset_data_values(self):
        
        self.model_extract.total_extract_count = 0
        self.model_extract.extract_list.clear()
        
        self.common_model.refresh_model()
        
    def hide_right_common(self):
        
        self.ui_inst.snap_gif.hide()
        self.ping_engine_object.ping_wind.main_widget.hide()
        self.config_engine_object.config_window.main_widget.hide()
#         self.compare_view_object.display_compare.main_widget.hide()
        
        
        
        
        