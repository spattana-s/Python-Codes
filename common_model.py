'''
Created on 12 June  2018

@author: sp977u@att.com  (Satish Palnati)

Pleases take care of logging part

'''
import os 


class common_options_model:

    def __init__(self,):
        
        self.user_name = "NF"
        self.psw = 'NF'
        self.cr_number = "NF"
        self.usr_name_given_flag  = "Red"
        self.psw_given_flag  = "Red"
        self.cr_given_flag = "Red"
        
        self.ipaddress_file = "NF"   # this contains real ip address file what user selects view
        self.ipaddress_file_selected = False
        self.ipadd_box_filled = False
        self.ipadd_box_content = ''  # bydefault it is zero
        
        self.final_ip_list = []
        self.invalid_ip_list = []
        self.duplicate_ip_list = []
        self.valid_ip_flag = 'Red'
        self.ip_address_input_flag  = "Red"
        
        self.command_file = "NF"
        self.command_file_selected = False
        self.command_file_list=[]  #  file commands are retained and useful for initial error handling
        self.commands_box_filled = False
        self.commands_box_content = ''  # zero size bydefault
        self.commands_input_flag = "Red"
        self.final_commands_list = []  # this is final list which is passed to command processor , also it includeds default list
        
        self.default_commands_set = False
        self.default_commands_list= []
                
        self.output_folder_selected = False
        self.output_path = os.getcwd()
        
        self.ping_only_selected = False
        self.flat_file_flg = 'NA'
        
        self.wlc_option = "No"
        
        self.proceed_signal = "Red"
    
    def refresh_model(self):
        self.ip_address_input_flag  = "Red"
        self.proceed_signal = "Red"
        self.commands_input_flag = "Red"
        self.default_commands_set = False
        self.ipaddress_file_selected = False
        self.ipadd_box_filled = False
        self.valid_ip_flag = 'Red'
        self.invalid_ip_list.clear()
        self.duplicate_ip_list.clear()
        self.command_file_selected = False
        self.commands_box_filled = False
        self.usr_name_given_flag  = "Red"
        self.psw_given_flag  = "Red"
        self.cr_given_flag = "Red"
        