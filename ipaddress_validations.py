'''
Created on 17 june, 2018

@author: sp977u@att.com  (Satish Palnati)

This class is written for validating IP addresses from both .txt file and  from input box on GUI . We collect both items and remove duplicates
and incorrect IP format strings to consider only valid IPv4 addresses.

'''
from PySide import QtGui
import string
import socket
import re
import datetime

class ipAddressValidate:

    def __init__(self,last_parent):
        
        self.last_parent = last_parent
        self.ip_add_file='NF'
        self.ip_box_content=''
        self.final_ip_list=[] #after removing blank lines and striping each line for spaces from ip_file_list
        self.ip_file_list=[] #contains all the data of file and content-box
        self.duplicate_ip=[]
        self.valid_ip=[]
        self.invalid_ip = []
   
    def check_valid_ip_addresses(self,ip_file,ip_box_content):
        
        self.ip_add_file=ip_file
        self.ip_box_content=ip_box_content
        self.intial_ip_list =[]
        self.final_ip_list.clear()
        self.ip_file_list.clear()
        self.duplicate_ip.clear()
        self.valid_ip.clear()
        self.invalid_ip.clear()
        boxcontent_list=[]
#          and self.last_parent.validations.common_model.ipaddress_file_selected == True 
        if self.ip_add_file != 'NF' and self.ip_add_file != "":
            try:
                with open(self.ip_add_file,'r') as ip_file:
                    self.ip_file_list = ip_file.readlines()
                    print("45 ipadd validations")
            except Exception as ex:
                print('There is something wrong with the IP-file opening operation in ipaddress_validation module \n', ex)
                self.last_parent.msgBox.critical(self.last_parent.gui,'Invalid File',"Unable to open IP Address file, Please check and retry...!", QtGui.QMessageBox.Ok)
                self.last_parent.base_left.go_button.setDisabled(False)
                
        
        if len(self.ip_box_content) >0 :
            boxcontent_list = self.ip_box_content.replace('\t', '\n').replace(',', "\n").replace(";", "\n").split('\n')
            
        
        self.ip_file_list= self.ip_file_list + boxcontent_list
        #self.last_parent.validations.common_model.final_ip_list = self.ip_file_list
        if len(self.ip_file_list) >0 :
            self.validate_ip()
        else :
            self.last_parent.msgBox.critical(self.last_parent.gui,'File Empty..!','No File or any IPs have been entered..!!', QtGui.QMessageBox.Ok)
            #log into file and display error
        
    
    def validate_ip(self):
        num_valid_ip = num_invalid_ip = 0
        all_ips=[]
        
        # list of invalid characters other than "." 
        invalidChars = list(string.punctuation.replace(".", "")) 
        
        # removing blank lines and striping each line for spaces
        for i in range(len(self.ip_file_list)):
            if self.ip_file_list[i] != '\n' :
                self.final_ip_list.append(self.ip_file_list[i].strip())
                all_ips.append(self.ip_file_list[i].strip())
                
        # Removing duplicates using set()
        self.final_ip_list = list(set(self.final_ip_list))
        
        for i in range(len(self.final_ip_list)):
            
        # conditions for NO "." in the line and an alphabet or a special character in the line
            if '.' not in self.final_ip_list[i] or re.search('[a-zA-Z]', self.final_ip_list[i]) or any(char in invalidChars for char in self.final_ip_list[i]):
                    self.invalid_ip.append(self.final_ip_list[i])
                    num_invalid_ip+=1
            else:
                try:
                    socket.inet_aton(self.final_ip_list[i])
                    self.valid_ip.append(self.final_ip_list[i])
                    num_valid_ip+=1
                    
                except socket.error:
                    self.invalid_ip.append(self.final_ip_list[i])
                    num_invalid_ip+=1
            
        self.duplicate_ip=list(set([x for x in all_ips if all_ips.count(x) > 1]))
        self.last_parent.validations.common_model.final_ip_list = self.valid_ip
        self.last_parent.validations.common_model.invalid_ip_list = self.invalid_ip
        self.last_parent.validations.common_model.duplicate_ip_list = self.duplicate_ip
        self.show_valids()
#         print ('\n\nThere are {} valid IPs\n\n'.format(num_valid_ip))
#         print(''.join(self.valid_ip))
#         print ('\n\nThere are {} invalid IPs\n\n'.format(num_invalid_ip))
#         print(''.join(self.invalid_ip))
#         print ('\n\nThere are {} duplicate IPs\n\n'.format(len(self.duplicate_ip)))
#         print(''.join(self.duplicate_ip))
#         
    def show_valids(self):
        
        self.output_path = self.last_parent.validations.common_model.output_path
        self.date_time = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H:%M:%S').replace(':','-')
        
        if len(self.valid_ip) >0:
            self.last_parent.validations.common_model.valid_ip_flag = 'Green'
            print("Ip validations 118")
            
            
        elif len(self.invalid_ip) > 0:
            self.last_parent.msgBox.critical(self.last_parent.gui,'No Valid IPs Found',"No valid IPs found , Please check the given IPs..!", QtGui.QMessageBox.Ok)
            self.last_parent.base_left.go_button.setDisabled(False)
            self.last_parent.validations.common_model.valid_ip_flag = 'Red'
            print("Ip validations 122")
        else:
            self.last_parent.msgBox.critical(self.last_parent.gui,'File Empty..!','No File or any IPs have been entered..!!', QtGui.QMessageBox.Ok)
            self.last_parent.base_left.go_button.setDisabled(False)
            self.last_parent.validations.common_model.valid_ip_flag = 'Red'       
        
            
        
        