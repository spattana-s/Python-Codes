'''
Created on 28 May  2018

@author: sp977u@att.com  (Satish Palnati)

'''
from PySide import QtGui
from PySide import QtCore
import os
import webbrowser as wb
from views.config.config_window import ConfigWindow
from views.ping.ping_window import PingWindow
class left_base:

    def __init__(self,last_parent): # last parent is instance of UI _MAIN VIEW class from ui_parent module
        
        
        self.last_parent = last_parent
        self.gui = last_parent.gui
        self.prepare_left_common()
        #self.ping_view = PingWindow(last_parent)
        #self.config_view = ConfigWindow(last_parent)
        self.connect_file_openers()  # binding file dialog methods
    
    def prepare_left_common(self):
        
        self.newfont = QtGui.QFont("Verdana", 9, QtGui.QFont.Normal)
        
        self.msgBox = QtGui.QMessageBox()
        self.msgBox.setWindowIcon(QtGui.QIcon(":/logo/Wind_icon.png"))
        self.msgBox.setFont(self.newfont)
        
# user name label        
        self.UsernameLab =  QtGui.QLabel()
        self.UsernameLab.setText("User ID :   ")
        self.UsernameLab.setFont(self.newfont)
        self.last_parent.username_layout_lb_h.addWidget(self.UsernameLab)
        self.UsernameLab.hide()
        
# save username
        self.saveUseranme = QtGui.QCheckBox()
        
        
# user name box
        self.UsernameBox = QtGui.QLineEdit()
        self.UsernameBox.setToolTip("Enter GTAC Username... !")
        self.UsernameBox.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 2px  }""")
        self.UsernameBox.setFont(self.newfont)
        self.UsernameBox.setObjectName("Username")
        if self.last_parent.save_username_checked == True: 
            print("came to left base save username if")
            username_file_handler = open('Username.txt','r')
            lines = username_file_handler.readlines()
            if len(lines):
                self.UsernameBox.setText(lines[0])
                self.last_parent.validations.common_model.user_name = lines[0]
            self.last_parent.validations.common_model.usr_name_given_flag = "Green"
        else:
            print("came to left base save username else")
            self.saveUseranme.setChecked(False)
            self.last_parent.validations.common_model.usr_name_given_flag = "Red"
        self.last_parent.username_layout_lb_h.addWidget(self.UsernameBox)
        self.UsernameBox.hide()      
# save username
        self.saveUseranme.setStyleSheet("color: blue;border: orange solid 2px")
        self.saveUseranme.setText("Remember Me")
        self.saveUseranme.setFont(QtGui.QFont("Verdana", 8, QtGui.QFont.Normal))
        self.saveUseranme.setObjectName("save_username")
        self.saveUseranme.setToolTip("Please select this option if you want to remember your GTAC Username .!")
        if self.last_parent.save_username_checked == True: 
            self.saveUseranme.setChecked(True)
        else:
            self.saveUseranme.setChecked(False)
        self.last_parent.username_layout_lb_h.addWidget(self.saveUseranme)
        self.saveUseranme.hide()
# user name error label
        self.username_error_label =  QtGui.QLabel() # error label
        self.username_error_label.setText("Enter a Username")
        self.username_error_label.setFont(self.newfont)
        self.username_error_label.setStyleSheet("color: red")
        self.last_parent.username_layout_lb_h.addWidget(self.username_error_label)
        self.username_error_label.hide()


                
# password label   
#         self.last_parent.password_layout_lb_h.addSpacing(-150)
        
        self.PassLab =  QtGui.QLabel()
        self.PassLab.setText("Password :")
        self.PassLab.setFont(self.newfont)
        self.PassLab.setAlignment(QtCore.Qt.AlignLeft)
        self.last_parent.password_layout_lb_h.addWidget(self.PassLab)
        self.PassLab.hide()
        
# password box         
        self.PassBox = QtGui.QLineEdit()
        self.PassBox.setToolTip("Enter GTAC Password.. !")
        self.PassBox.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 2px  }""")
        self.PassBox.setFont(self.newfont)
        self.PassBox.setObjectName("pass")
        self.PassBox.setEchoMode(QtGui.QLineEdit.Password)
        self.last_parent.password_layout_lb_h.addWidget(self.PassBox)
        self.last_parent.password_layout_lb_h.setAlignment(QtCore.Qt.AlignLeft)
        self.PassBox.hide()
        
# password error label        
        self.pass_error_label =  QtGui.QLabel() # error label
        self.pass_error_label.setText("Enter a password")
        self.pass_error_label.setFont(self.newfont)
        self.pass_error_label.setStyleSheet("color: red")
        self.last_parent.password_layout_lb_h.addWidget(self.pass_error_label)
        self.pass_error_label.hide()
        
# ip address labels and boxes 

        self.ip_file_input_label =  QtGui.QLabel()
        self.ip_file_input_label.setText("IP Address File : " )
        self.ip_file_input_label.setFont(self.newfont)
        self.last_parent.ip_file_select_layout_lb_h.addWidget(self.ip_file_input_label)
        self.ip_file_input_label.hide()
        
               
        self.ipaddress_file_btn = QtGui.QPushButton("Select")
        self.ipaddress_file_btn.setFont(self.newfont)
        self.ipaddress_file_btn.setMinimumWidth(100)
        self.ipaddress_file_btn.setMaximumWidth(100)
        self.ipaddress_file_btn.setObjectName("ipaddress_file")
        self.ipaddress_file_btn.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 2px  }""")
        self.ipaddress_file_btn.setToolTip("Please select IP address file as Input for processing...")
        self.last_parent.ip_file_select_layout_lb_h.addWidget(self.ipaddress_file_btn)
        self.ipaddress_file_btn.hide()
        
        self.ip_add_box = QtGui.QTextEdit()
        self.ip_add_box.setMaximumHeight(50)
        self.ip_add_box.setToolTip("Enter IP Addresses here .. !")
        self.ip_add_box.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 2px  }""")
        self.ip_add_box.setFont(self.newfont)
        self.ip_add_box.setObjectName("IP_Address")
        self.last_parent.ip_file_layout_lb_v.addWidget(self.ip_add_box)
        self.ip_add_box.hide()
    
        self.ipadd_file_error_label =  QtGui.QLabel() # error label
        self.ipadd_file_error_label.setText("Select IP address file or enter IP details in the box provided ..!")
        self.ipadd_file_error_label.setFont(self.newfont)
        self.ipadd_file_error_label.setStyleSheet("color: red")
        self.last_parent.ip_file_layout_lb_v.addWidget(self.ipadd_file_error_label)
        self.ipadd_file_error_label.hide()
        
        self.ipadd_file_name_label =  QtGui.QLabel() # file name label
        self.ipadd_file_name_label.setFont(self.newfont)
        self.ipadd_file_name_label.setStyleSheet("color: green")
        self.last_parent.ip_file_select_layout_lb_h.addWidget(self.ipadd_file_name_label)
        self.ipadd_file_name_label.hide()
        
# commands label defaults     
        self.default_commands_chbx = QtGui.QCheckBox()  # for toggle option for commands 
        self.default_commands_chbx.setStyleSheet("color: blue;border: orange solid 2px")
        self.default_commands_chbx.setText("Default Commands")
        self.default_commands_chbx.setFont(self.newfont)
        self.default_commands_chbx.setObjectName("default_commands")
        self.default_commands_chbx.setToolTip("Please select this option if you want to run default show commands .!")
        self.default_commands_chbx.setChecked(True)
        self.last_parent.default_chkbx_layout_lb_h.addWidget(self.default_commands_chbx)
        self.default_commands_chbx.hide()        
        
        
        self.commands_file_radio = QtGui.QRadioButton()
        self.commands_file_radio.setStyleSheet("color: blue;border: orange solid 2px")
        self.commands_file_radio.setText("Commands TXT File  ")
        self.commands_file_radio.setFont(self.newfont)
        self.commands_file_radio.setObjectName("commands_file")
        self.commands_file_radio.setToolTip("Please select this option if you want to select commands .txt file .!")
        self.last_parent.commands_file_layout_lb_h.addWidget(self.commands_file_radio)
        self.commands_file_radio.hide()        
        
        
        self.commands_file_btn = QtGui.QPushButton()
        self.commands_file_btn.setText("Select")
        self.commands_file_btn.setMinimumWidth(100)
        self.commands_file_btn.setMaximumWidth(100)
        self.commands_file_btn.setFont(self.newfont)
        self.commands_file_btn.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.commands_file_btn.setObjectName("commands_file")
        self.commands_file_btn.setToolTip("Please select Commands file or enter commands as Input for processing...")
        self.commands_file_btn.setDisabled(True)
        self.last_parent.commands_file_layout_lb_h.addWidget(self.commands_file_btn)
        self.commands_file_btn.hide()
        
        self.cmds_filename_label =  QtGui.QLabel() # error label
        self.cmds_filename_label.setText("No file selected..!")
        self.cmds_filename_label.setFont(self.newfont)
        self.cmds_filename_label.setStyleSheet("color: red")
        self.last_parent.commands_file_layout_lb_h.addWidget(self.cmds_filename_label)
        self.cmds_filename_label.hide()
        
        self.commands_custom_radio = QtGui.QRadioButton()  # for toggle option for commands 
        self.commands_custom_radio.setStyleSheet("color: blue;border: orange solid 2px")
        self.commands_custom_radio.setText("Custom Commands  ")
        self.commands_custom_radio.setFont(self.newfont)
        self.commands_custom_radio.setObjectName("commands_opt_toggle")
        self.commands_custom_radio.setToolTip("Please select this option if you want to enter commands in input box provided .!")
        self.commands_custom_radio.setChecked(False)
        self.last_parent.commands_custom_box_layout_lb_h.addWidget(self.commands_custom_radio)
        self.commands_custom_radio.hide()


        self.commands_box = QtGui.QTextEdit()
        self.commands_box.setMaximumHeight(40)
        self.commands_box.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.commands_box.setToolTip("Enter Commands to run .. !")
        self.commands_box.setFont(self.newfont)
        self.commands_box.setObjectName("Commands_box")
        self.commands_box.setDisabled(True)
        self.last_parent.commands_custom_box_layout_lb_h.addWidget(self.commands_box)
        self.commands_box.hide()
        
        self.none_radio = QtGui.QRadioButton()  # for toggle option for commands 
        self.none_radio.setStyleSheet("color: blue;border: orange solid 2px")
        self.none_radio.setText("None  ")
        self.none_radio.setFont(self.newfont)
        self.none_radio.setObjectName("commands_opt_toggle")
        self.none_radio.setToolTip("Please select this option if you want reset the commands selection ...!")
        self.none_radio.setChecked(True)
        self.last_parent.none_radio_btn_layout_lb_h.addWidget(self.none_radio)
        self.none_radio.hide()
        
        self.cmds_error_label =  QtGui.QLabel() # error label
#         self.cmds_error_label.setText("Select IP address file or enter IP details in the box provided ..!")
        self.cmds_error_label.setFont(self.newfont)
        self.cmds_error_label.setStyleSheet("color: red")
        self.last_parent.commands_label_layout_lb_v.addWidget(self.cmds_error_label)
        self.cmds_error_label.hide()
        
# Output options       

        self.output_folder_label =  QtGui.QLabel()
        self.output_folder_label.setText("Open Output Folder : " )
        self.output_folder_label.setFont(self.newfont)
        self.last_parent.output_layout_lb_h.addWidget(self.output_folder_label)
        self.output_folder_label.hide()
        
        self.open_out_folder_btn = QtGui.QPushButton("Open")
        self.open_out_folder_btn.setMinimumWidth(100)
        self.open_out_folder_btn.setMaximumWidth(100)
        self.open_out_folder_btn.setFont(self.newfont)
        self.open_out_folder_btn.setObjectName("destination_folder")
        self.open_out_folder_btn.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.open_out_folder_btn.setToolTip("Please click to open output folder !")
        self.last_parent.output_layout_lb_h.addWidget(self.open_out_folder_btn)
        self.open_out_folder_btn.hide()
        
        
# common single button for 4 options

        self.go_btn_font = QtGui.QFont("Verdana", 9, QtGui.QFont.Bold)
        
        self.go_button = QtGui.QPushButton()
        self.go_button.setObjectName("go_button")
        self.go_button.setMinimumHeight(30)
        self.go_button.setMinimumWidth(200)
        self.go_button.setMaximumWidth(200)
        self.go_button.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.go_button.setFont(self.go_btn_font)
        self.go_button.setToolTip('Please select required fields before clicking this button...!')
        self.last_parent.go_btn_layout_lb_h.addWidget(self.go_button)
        self.go_button.hide()
        
        self.create_get_specific() 
        self.create_push_specific()
        
        
    def create_get_specific(self):
        # get ping logs ;  off by default
        
        self.get_ping_logs_chbx = QtGui.QCheckBox()
        self.get_ping_logs_chbx.setText("Get Ping Logs ONLY")
        self.get_ping_logs_chbx.setFont(self.newfont)
        self.get_ping_logs_chbx.setObjectName("onlyping_logs")
        self.get_ping_logs_chbx.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.get_ping_logs_chbx.setToolTip("Please select this option if you want only ping logs to be generated...!")
        self.get_ping_logs_chbx.setChecked(False)
        self.last_parent.results_layout_lb_v.addWidget(self.get_ping_logs_chbx)
        self.get_ping_logs_chbx.hide()
        
        self.get_conf_logs_chbx = QtGui.QCheckBox()
        self.get_conf_logs_chbx.setText("Get Config AND Ping Logs")
        self.get_conf_logs_chbx.setFont(self.newfont)
        self.get_conf_logs_chbx.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.get_conf_logs_chbx.setObjectName("get_config_logs")
        self.get_conf_logs_chbx.setToolTip("Please select this option if you want to capture config and ping logs...!")
        self.last_parent.results_layout_lb_v.addWidget(self.get_conf_logs_chbx)
        self.get_conf_logs_chbx.hide()
        
        self.get_config_flatfile_chbx = QtGui.QCheckBox()
        self.get_config_flatfile_chbx.setText("Get Flat File For Configuration Logs")
        self.get_config_flatfile_chbx.setFont(self.newfont)
        self.get_config_flatfile_chbx.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 1px  }""")
        self.get_config_flatfile_chbx.setObjectName("get_flat_config_logs")
        self.get_config_flatfile_chbx.setToolTip("Please select this option if you want to capture a flat file of all IPs config logs...!")
        self.last_parent.results_layout_lb_v.addWidget(self.get_config_flatfile_chbx)
        self.get_config_flatfile_chbx.hide()
        
    def create_push_specific(self):
        
        self.cr_label = QtGui.QLabel(self.gui)
        self.cr_label.setText("CR Number : ")
        self.cr_label.setObjectName("CR_Label")
        self.last_parent.cr_layout_lb_h.addWidget(self.cr_label)
        self.cr_label.hide()
        
        self.cr_box = QtGui.QLineEdit()
        self.cr_box.setToolTip("Enter the mandatory TSRM CR Number.. !")
        self.cr_box.setObjectName("CR_Box")
        self.cr_box.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 2px  }""")
        self.last_parent.cr_layout_lb_h.addWidget(self.cr_box)
        self.cr_box.hide()
        
        self.cr_error_label =  QtGui.QLabel() # error label
        self.cr_error_label.setText("Please enter CR number ..!")
        self.cr_error_label.setFont(self.newfont)
        self.cr_error_label.setStyleSheet("color: red")
        self.last_parent.ip_file_layout_lb_v.addWidget(self.cr_error_label)
        self.cr_error_label.hide()
    
    def show_left_common(self):
        
        self.UsernameLab.show()
        self.UsernameBox.show()
        self.saveUseranme.show()
        self.PassLab.show()
        self.PassBox.show()
        self.ip_file_input_label.show()
        self.ipaddress_file_btn.show()
        self.ip_add_box.show()
        self.default_commands_chbx.show()
        self.commands_file_radio.show() 
        self.commands_custom_radio.show()
        self.none_radio.show()
        self.commands_file_btn.show()
        self.commands_box.show()
        self.output_folder_label.show()
        self.open_out_folder_btn.show()
        self.default_commands_chbx.show()
        self.output_folder_label.show()
        self.open_out_folder_btn.show()
        
    def connect_file_openers(self,):
        
        
        self.open_out_folder_btn.clicked.connect(self.open_output_folder)
        self.commands_file_btn.clicked.connect(self.select_commands_file)
        self.ipaddress_file_btn.clicked.connect(self.select_ipadd_file)
         
        self.commands_custom_radio.clicked.connect(self.toggle_commands_option)
        self.commands_file_radio.clicked.connect(self.toggle_commands_option)
        self.none_radio.clicked.connect(self.toggle_commands_option)
        self.get_ping_logs_chbx.stateChanged.connect(self.enable_ping_only_controls)
        self.get_config_flatfile_chbx.stateChanged.connect(self.enable_flat_file_control)
    
    
    def open_output_folder(self):
        
        try:
            wb.open(self.last_parent.validations.common_model.output_path)
        
        except Exception as ex:
            print("Exception : " ,ex)
            print("left base view line 316")
        
    def select_ipadd_file(self):    
        self.ipaddfile = "NF"
        prob_flag = False
        filename = "NF"
    
        try :
            
            self.ipadd_file_error_label.hide()
            self.ipaddfile = QtGui.QFileDialog.getOpenFileName(self.gui, 'Select IP Address file')
            self.ipaddfile = self.ipaddfile[0]
            self.last_parent.validations.common_model.ipaddress_file =   self.ipaddfile[:]   # updating common model variable using class var ipadd file
            
            if self.last_parent.validations.common_model.ipaddress_file != "NF" :
                
                if ".txt" in self.ipaddfile.lower() :
                    filename = "File selected : " + self.ipaddfile[self.ipaddfile.rfind("/") +1 : ]
                    self.ipadd_file_name_label.setText(filename)
                    self.ipadd_file_name_label.show()
                    self.ipadd_file_name_label.setStyleSheet("color: green")
                    print("Left_base View line 276")
                    
                    
                    if os.path.isfile(self.ipaddfile):
                        print(self.ipaddfile)
                        print("Left_base View line 302")
                    else:
                        self.msgBox.critical(self.gui,'Error!',"Unable to open IP Address file, Please check and retry...!", QtGui.QMessageBox.Abort)
                        prob_flag = True
                        self.ipaddfile = "NF"
                        self.ipadd_file_error_label.setStyleSheet("color: red")
                        self.ipadd_file_error_label.setText("Select IP address file or enter IP details in the box provided ..!")
                        self.last_parent.validations.common_model.ipaddress_file_selected = False
                        self.last_parent.validations.common_model.ipaddress_file  = "NF"
                        print("Left_base View line 311")
                    
                elif len(self.last_parent.validations.common_model.ipaddress_file) >0:
                    filename = "File selected : " + self.ipaddfile[self.ipaddfile.rfind("/") +1 : ]
                    self.ipadd_file_name_label.setText(filename)
                    self.ipadd_file_name_label.show()
                    self.ipadd_file_name_label.setStyleSheet("color: red")
                    self.last_parent.msgBox.critical(self.last_parent.gui,'Input Error',"Please select correct file type (.txt) which contains valid IP addresses..!", QtGui.QMessageBox.Ok)
                    print("Left_base View line 284")
                else:
                    self.ipadd_file_error_label.hide()
                    self.ipadd_file_name_label.hide()
                    self.msgBox.critical(self.gui,'Error!',"Unable to open IP Address file, Please check and retry...!", QtGui.QMessageBox.Abort)
                    self.last_parent.validations.common_model.ipaddress_file =  "NF" # updating model class var ipadd file
                    print("Left_base View line 288")
                    
                print("Left_base View line 298")
                print(self.last_parent.validations.common_model.ipaddress_file)
            
                
            else:
                print("Left_base View line 354")
#                 self.ipadd_file_name_label.hide()
#                 self.last_parent.validations.common_model.ipaddress_file_selected = False
#                 self.last_parent.common_model.ipaddress_file = "NF" 
                 
        except TypeError:
            self.ipaddfile = "NF"
            self.last_parent.validations.common_model.ipaddress_file  = "NF"

        except Exception as uex:
            self.ipaddfile ="NF"
            self.msgBox.critical(self.gui,'Error!',"1 Unable to open IP Address file, Please check and retry...!", QtGui.QMessageBox.Abort)
            prob_flag = True
            print(uex)
            self.last_parent.validations.common_model.ipaddress_file  = "NF"
            
        if prob_flag == True :
            self.go_button.setDisabled(False) 
            print("Left_base View line 332")
            
    def select_commands_file(self):    
        
        prob_flag = False
        self.commands_file = "NF"
        filename = "NF"
        
        try :
            cmdfile = QtGui.QFileDialog.getOpenFileName(self.gui, 'Select commands file')
            self.commands_file = cmdfile[0]
            self.last_parent.validations.common_model.command_file =   self.commands_file[:] # we are mapping file name to model class variable
            
            if len(self.commands_file) >0  :

                filename = "File selected : " + self.commands_file[ self.commands_file.rfind("/") +1 : ]
                if ".txt" in self.commands_file.lower() :
                    self.last_parent.validations.common_model.command_file =   self.commands_file[:]  # updating model class var ipadd file
                    self.last_parent.validations.common_model.command_file_selected = True
                    print("Left_base View line 356")
                    self.cmds_filename_label.setStyleSheet("color: green")
                    self.cmds_filename_label.setText(filename)
                    self.cmds_filename_label.show()
                    self.cmds_error_label.hide()
                     
                else: 
                    self.last_parent.validations.common_model.command_file =  "NF" # updating model class var ipadd file
                    self.last_parent.validations.common_model.command_file_selected = False
                    self.cmds_filename_label.setStyleSheet("color: red")
                    self.cmds_filename_label.setText(filename)
                    self.cmds_filename_label.show() 
                    self.cmds_error_label.setStyleSheet("color: red")
                    self.cmds_error_label.setText(" Please Select a \".txt\"  File..!")
                    self.cmds_error_label.show()
                    self.msgBox.critical(self.last_parent.gui,'Invalid File',"Unable to open Commands file, Please Select a \".txt\"  File and retry...!", QtGui.QMessageBox.Ok)
                    print("Left_base View line 360")
                    
            elif self.commands_file == '':
                self.cmds_filename_label.hide()
                prob_flag = True
                self.commands_file = "NF"   
                self.last_parent.validations.common_model.command_file = "NF"
                self.cmds_error_label.setStyleSheet("color: red")
                self.cmds_error_label.setText("Select Commands file or enter Command details in input box provided ..!")
                self.cmds_error_label.show()
                self.msgBox.critical(self.gui,'Error!',"Unable to open commands file, Please check and retry...!", QtGui.QMessageBox.Abort)
                
        except TypeError:
            self.commands_file = "NF"
            self.last_parent.validations.common_model.command_file = "NF"
            self.cmds_error_label.setStyleSheet("color: red")
            self.cmds_error_label.setText("Select Commands file or enter Command details in input box provided ..!")
#             self.cmds_error_label.show()
            pass
        
        except Exception as ex:
            print("excpetion",ex)
            self.commands_file ="NF"
            self.last_parent.validations.common_model.command_file = "NF"
            self.msgBox.critical(self.gui,'Error!',"Unable to open commands file, Please check and retry...!", QtGui.QMessageBox.Abort)
            prob_flag = True
            
            self.cmds_error_label.setStyleSheet("color: red")
            self.cmds_error_label.setText("Select Commands file or enter Command details in input box provided ..!")
#             self.cmds_error_label.show()
            
            if filename == "NF":
                self.cmds_error_label.hide()
    
            print("Open the file  correctly...!")
        if prob_flag == True :
            self.go_button.setDisabled(False) 
            
    def toggle_commands_option(self):
        if self.commands_custom_radio.isChecked():
            self.commands_box.setDisabled(False)

            self.commands_file_btn.setDisabled(True)
            self.cmds_error_label.hide()
            
        if self.commands_file_radio.isChecked():
            self.commands_box.setDisabled(True)
            self.commands_file_btn.setEnabled(True)
            if self.last_parent.validations.common_model.command_file != "NF" :
                self.cmds_error_label.setHidden(False)
            self.cmds_error_label.hide()
                
        if self.none_radio.isChecked():
            self.commands_box.setDisabled(True)
            self.commands_file_btn.setDisabled(True)
            self.cmds_error_label.hide()
        
        
        
    def enable_ping_only_controls(self):
        if self.get_ping_logs_chbx.isChecked():
            self.last_parent.credentials_groupbox.setDisabled(True)
            self.get_conf_logs_chbx.setDisabled(True)
            self.get_conf_logs_chbx.setChecked(False)
            self.last_parent.Commands_groupBox.setDisabled(True)
            self.get_config_flatfile_chbx.setDisabled(True)
            self.get_config_flatfile_chbx.setChecked(False)
            self.last_parent.validations.common_model.ping_only_selected = True
            
            
        elif not self.get_ping_logs_chbx.isChecked():
            
            self.last_parent.credentials_groupbox.setDisabled(False)
            self.get_conf_logs_chbx.setDisabled(False)
            self.get_conf_logs_chbx.setChecked(True)
            self.last_parent.Commands_groupBox.setDisabled(False)
            self.get_config_flatfile_chbx.setDisabled(False)
            self.last_parent.validations.common_model.ping_only_selected = False
            
            
    
    def enable_flat_file_control(self):
        
        if self.get_config_flatfile_chbx.isChecked():
            self.last_parent.validations.common_model.flat_file_flg =  "True" 
        else:
            self.get_config_flatfile_chbx.setChecked(False)
            self.last_parent.validations.common_model.flat_file_flg = "NA"
            
            
            