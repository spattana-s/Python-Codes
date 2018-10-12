'''
Created on 15 june, 2018
@author: sp977u@att.com  (Satish Palnati)
This class is for starting process to create threads and kick start process.
We validate the model class data and prepare correct sets . once we have correct data, we can call respective functionality.
we instantiate Service classes under service network package. 

'''
from PySide import QtCore,QtGui
from service_network.pingLogprocess import PingProcessor
import os 
import time
import datetime
import threading
from views.ping.ping_window import PingWindow


class PingEngine:
    
    quit_flag = False
    
    
    def __init__(self,common_model,last_parent):
        self.totalcount = 0
        self.common_model = common_model
        self.signalcount = 0
        self.threadPool = QtCore.QThreadPool()
        self.lock = threading.Lock()
        self.threadPool.setMaxThreadCount(48)
        
        
        self.last_parent =  last_parent
        
        self.ping_wind = PingWindow(last_parent) # to prepare GUI ping components for right base layout
        
    def start_ping_engine(self):
        
        #self.close_right_child_widgets()
        #self.ping_wind.main_widget.show()
        
        self.date_time = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H:%M:%S').replace(':','-')
        if self.common_model.valid_ip_flag == 'Green':
            try :  
                    os.makedirs(self.common_model.output_path + "\\"+ self.date_time)  # put folder name as per view selected
                    self.PingLogfile_path =  self.common_model.output_path + "\\"+ self.date_time +  "\\ping_log.txt"
                    self.PingLogfile_hand = open(self.PingLogfile_path,'w+')    
                    
                    self.PingLogfile_hand.write("Valid IP : " + str(len(self.common_model.final_ip_list)) + "\n\n")
                    self.PingLogfile_hand.write("InValid IP : " + str(len(self.common_model.invalid_ip_list)) + "\n\n")
                    self.PingLogfile_hand.write("Duplicate IP : " + str(len(self.common_model.duplicate_ip_list)) + "\n\n")
                    
            except TypeError :
                self.common_model.output_path = self.common_model.output_path.decode('utf-8')
                os.makedirs(self.common_model.output_path + "\\"+ self.date_time)
                
            except Exception as uex:
                print("error:", uex)
                print( 'unable to create output folder. Please check the disk space or permissions!')
                #log to file
                #pop-up
                return 0
            
            self.ping_wind.prepare_window()
 
            self.ping_wind.cancel_button.clicked.connect(self.cancel_all)
            
            self.ping_wind.progressBar.setValue(0)
            
            for ip in self.common_model.final_ip_list:
                self.qtcmd = PingProcessor(ip, self.common_model.output_path + "\\" + self.date_time +"\\",len(self.common_model.final_ip_list),'True',self.PingLogfile_hand,self)
                self.qtcmd.finishedProcessing.connect(self.pingbarUpdate)
                self.threadPool.start(self.qtcmd)
    
        
  
        
    def pingbarUpdate(self,totalcount,ip_status):
        
    
        try:
            if self.ping_wind.wind_close_flg == True:
                self.quit_flag = True
                self.last_parent.base_left.go_button.setDisabled(False)
            
            self.lock.acquire()
            self.signalcount +=1
            
            self.ping_wind.progressBar.setValue(self.signalcount*100/totalcount)
            self.ping_wind.progressBar.show()
            
            #self.ping_wind.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
            
            
    
            if ": Down" in ip_status:
                
                ipstatus = ip_status.replace(": Down",'')
                self.ping_wind.down_ip_textbox.appendPlainText(ipstatus)
                
            elif ": Up" in ip_status :
                
                ipstatus = ip_status.replace(": Up",'')
                self.ping_wind.up_ip_textbox.appendPlainText(ipstatus)
                
            elif "Cancelled"  in ip_status:
                self.ping_wind.progressLabel.setText("Ping log process is being Cancelled,  Please wait ....!")
    #             self.threadPool.waitForDone()
                #print("Current active : ",self.threadPool.activeThreadCount())
                
                pass
            
                #self.ping_wind.down_ip_textbox.appendPlainText(ip_status)
            
            if self.signalcount >= totalcount:
                self.ping_wind.progressBar.hide()
                self.ping_wind.progressLabel.hide()
                self.last_parent.base_left.go_button.setDisabled(False)
                self.ping_wind.cancel_button.hide()
    #             if "Cancelled"  in ip_status:
    #                 self.last_parent.msgBox.information(None,'Job status!',"Ping logs process has  been cancelled.!", QtGui.QMessageBox.Ok)
    #                 self.signalcount = 0
                if self.quit_flag == False:
                    self.last_parent.msgBox.information(self.last_parent.gui,'Job status!',"Ping logs have been completed, Please check the log file..!", QtGui.QMessageBox.Ok)
                
                elif self.quit_flag == True and self.ping_wind.wind_close_flg == False:
                    self.last_parent.msgBox.information(self.last_parent.gui,'Job status!',"Ping logs process has  been cancelled.!", QtGui.QMessageBox.Ok)
                
                self.signalcount = 0
                
                #self.ping_wind.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
                
                self.quit_flag = False
                
            self.lock.release()
        
        except Exception as uexx:
            print("Unwanted error : ", uexx) 
        
    def cancel_all(self):
        
        self.quit_flag = True
        
        self.ping_wind.cancel_button.hide()
        
#         print("Current  active threads are :  ",self.threadPool.activeThreadCount())
        self.qtcmd.cancel_sig.emit("Cancel Job")
    
        #self.last_parent.msgBox.information(None,'Job status!',"Ping logs process has  been closed.!", QtGui.QMessageBox.Ok)
        
    '''def close_right_child_widgets(self):
        self.ping_wind.main_widget.hide()
        self.last_parent.right_base.hide()
        
        
    def start_config_engine(self):
        xyz = ['/','--','\\','|']
        print("entered Config engine")
        self.close_right_child_widgets()
        self.last_parent.right_base.show()
        self.last_parent.right_base.append("Configurations will be done here : ")
        for i in range(10):
            self.last_parent.right_base.append("Working on device "+ str(i)+"...")'''

        
            
            
        

            
        
    
