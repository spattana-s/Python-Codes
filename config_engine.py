'''
Created on 15 june, 2018
@author: sp977u@att.com  (Satish Palnati)
This class is for starting process to create threads and kick start process.
We validate the model class data and prepare correct sets . once we have correct data, we can call respective functionality.
we instantiate Service classes under service network package. 

'''
from PySide import QtCore,QtGui
import os 
import time
import datetime
import threading
from service_network.device_wheels.CommandProcessor import CommandProcessor
from service_network.device_wheels.MyProgressBar import MyProgressBar
from views.config.config_window import ConfigWindow
from validations.validateCredent import validateCredent

class ConfigEngine:
    
    quit_flag = False

    def __init__(self,common_model,last_parent):
        self.common_model = common_model
        self.signalcount = 0
        self.threadPool = QtCore.QThreadPool()
        self.lock = threading.Lock()
        self.threadPool.setMaxThreadCount(48)
    
        self.last_parent =  last_parent
        self.progress = MyProgressBar(len(self.common_model.final_ip_list))
        self.config_window = ConfigWindow(last_parent)
        
    
    def start_config_engine(self):
        self.signalcount = 0
        self.progress.totalCount = len(self.common_model.final_ip_list)
        self.progress.Duplicates = self.common_model.duplicate_ip_list
        
        self.progress.startTime = datetime.datetime.now().replace(microsecond=0)  # updating new time
        
        self.config_window.progressBar.setRange(0,self.progress.totalCount)
        
        
        self.gif_path = "C:/Users/rg012f/eclipse-workspace/speed tool rohan naya/credential_scanning.gif"
        self.last_parent.show_gif_right_base(self.gif_path,self.last_parent.right_base_layout_v)
       
        # Initial screening of credentials before proceeding for main job:
        self.cred_validate = validateCredent(self.common_model.final_ip_list, self.common_model.user_name, self.common_model.psw) # for  cred validat
        self.cred_validate.validate_signl.connect(self.kick_main_process)
        self.threadPool.start(self.cred_validate)
        

          
    
    def kick_main_process(self,credentResult,credTestpass ):
        
        
        
        print("\n\n Cred pass result : ",credentResult)
        
        if "Invalid username or Password" in credentResult :
            self.last_parent.hide_gif_right_base()
            self.last_parent.snap_gif.show()
            self.last_parent.msgBox.critical(self.last_parent.gui,'Error!',"Invalid Username or Password ,  Please check and try again...!", QtGui.QMessageBox.Abort)    
            #self.resetAllbuttons()
            self.last_parent.base_left.go_button.setDisabled(False)
            print("Credential result :  line 60 from config engine ",credentResult,credTestpass)
            
            
            return 0    
        
        if credTestpass == "Fail":
            self.last_parent.hide_gif_right_base()
            self.last_parent.snap_gif.show()
            self.last_parent.msgBox.critical(self.last_parent.gui,'Error!',"There is something wrong with reachability or credentials,  Please check and try again...!", QtGui.QMessageBox.Abort)    
            #self.resetAllbuttons()
            self.last_parent.base_left.go_button.setDisabled(False)
            print("Credential result :  line 67 from config engine ",credentResult,credTestpass)

            return 0
        
        self.last_parent.hide_gif_right_base()
       
        #print("Credential result :  line 61 from config engine ",self.credentRes,credTestpass)
         
        self.date_time = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H:%M:%S').replace(':','-')
        if self.common_model.valid_ip_flag == 'Green' and credTestpass == "Passed":
            
            self.config_window.prepare_window()
            self.last_parent.base_left.go_button.setDisabled(True)
            
            try :  
                os.makedirs(self.common_model.output_path + "\\"+ self.date_time)  # put folder name as per view selected
                
                '''self.PingLogfile_path =  self.common_model.output_path + "\\"+ self.date_time +  "\\ping_log.txt"
                self.PingLogfile_hand = open(self.PingLogfile_path,'w+')    
                
                self.PingLogfile_hand.write("Valid IP : " + str(len(self.common_model.final_ip_list)) + "\n\n")
                self.PingLogfile_hand.write("InValid IP : " + str(len(self.common_model.invalid_ip_list)) + "\n\n")
                self.PingLogfile_hand.write("Duplicate IP : " + str(len(self.common_model.duplicate_ip_list)) + "\n\n")'''
                
                
                Final_log_path = self.common_model.output_path + "\\"+ self.date_time +  "\\Final_log.txt"
                final_log_file = open(Final_log_path,"w+")
                final_log_file.write("****************************************************************************************\n")
                final_log_file.write(" Please check the status of below devices whether success or fail ...!\n")
                final_log_file.write("***************************************************************************************\n\n\n")
       
        
                final_log_file.write("Total Valid IP addresses given :  ")
                final_log_file.write(str(len(self.common_model.final_ip_list)))
                final_log_file.write("\n\n")
                
                final_log_file.close()
                    
                print("Flat flag : ",self.common_model.flat_file_flg)
                
                if self.common_model.flat_file_flg == "True" :
                    
                    flatOutputFile = self.common_model.output_path + "\\" + self.date_time +  "\\Matches_Found_All.txt"
                    SingleOutfile=  open(flatOutputFile,"w")
                                           
                    SingleOutfile.write("\n\n")
                    SingleOutfile.write("Below are the Matches Found :\n\n\n")
                    SingleOutfile.close()
                    
                    
                    
                    
            except TypeError :
                self.common_model.output_path = self.common_model.output_path.decode('utf-8')
                os.makedirs(self.common_model.output_path + "\\"+ self.date_time)
                
            except Exception as uex:
                print("error:", uex)
                print( 'unable to create output folder. Please check the disk space or permissions!  ( error location: line 76 in config engine...)')
                #log to file
                #pop-up
                return 0
            
            # enable this code later once we are done with GUI 
            
            self.config_window.prepare_window()
            self.config_window.progressBar.setValue(0)
            self.config_window.progressBar.setRange(0,100)
            self.config_window.cancel_button.clicked.connect(self.cancel_all)
            
            for ip in self.common_model.final_ip_list:
                self.qtcmd = CommandProcessor(ip,self.progress,self.common_model.user_name,self.common_model.psw, self.common_model.output_path + "\\" + self.date_time +"\\", self.common_model.final_commands_list,  len(self.common_model.final_commands_list), self.common_model.flat_file_flg, self.common_model.wlc_option, "N" , len(self.common_model.final_ip_list), self.common_model.default_commands_set)
                self.qtcmd.finishedProcessing.connect(self.progbarUpdate)
                self.threadPool.start(self.qtcmd)
    
          
  
        
    def progbarUpdate(self,totalcount,device_finish_count,ipadd):
        
    
        try:
            '''if self.ping_wind.wind_close_flg == True:
                self.quit_flag = True
                self.last_parent.base_left.go_button.setDisabled(False)'''
            
            self.lock.acquire()
            self.signalcount +=1
            self.config_window.progressBar.setValue(self.signalcount*100/totalcount)
            print("I have reached Bar update and Sig count is : ",self.signalcount)
#             self.config_window.config_textbox.append("I have reached Bar update and Sig count is : "+device_finish_count)
            config_string = str("Device with IP : "+str(ipadd)+" Completed ; "+str(totalcount-device_finish_count)+ " Remaining\n")
            
            if totalcount-device_finish_count == 0:
                self.config_window.config_textbox.appendPlainText("Device with IP : "+str(ipadd)+" Completed ; Shubhakanksha, Pani Sampurna\n")
            else :
                self.config_window.config_textbox.appendPlainText(config_string)
            if self.signalcount >= totalcount:
                #self.ping_wind.progressBar.hide()
                #self.ping_wind.progressLabel.hide()
                self.last_parent.base_left.go_button.setDisabled(False)
                #self.ping_wind.cancel_button.hide()
    #             if "Cancelled"  in ip_status:
    #                 self.last_parent.msgBox.information(None,'Job status!',"Ping logs process has  been cancelled.!", QtGui.QMessageBox.Ok)
    #                 self.signalcount = 0
                if self.quit_flag == False:
                    self.last_parent.msgBox.information(self.last_parent.gui,'Job status!',"Configuration logs have been completed, Please check the log file..!", QtGui.QMessageBox.Ok)
                    self.config_window.progressLabel.setText("Commands Processing Completed...:D Please Check the Log Files...!")
                elif self.quit_flag == True and self.ping_wind.wind_close_flg == False:
                    self.last_parent.msgBox.information(self.last_parent.gui,'Job status!',"Configuration logs process has  been cancelled.!", QtGui.QMessageBox.Ok)
                
                self.signalcount = 0
                
                #self.ping_wind.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
                
                self.quit_flag = False
                
            self.lock.release()
        
        except Exception as uexx:
            print("Unwanted error : ", uexx) 
    
    
    
        
        
    def cancel_all(self):
        
        self.quit_flag = True
        
        self.config_window.cancel_button.hide()
        
        self.qtcmd.cancel_sig.emit("Cancel Job")
    
    
   

        
    
