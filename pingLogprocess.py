'''
Created on July 23, 2017

@author: sp977u@att.com  (Satish Palnati)
'''

import sys
import re
import os
import subprocess
import copy
import time
from PySide import QtCore
from PySide.QtCore import QThread
import threading

class PingProcessor(QtCore.QObject,QtCore.QRunnable):
    
    finishedProcessing = QtCore.Signal(int,str)
    cancel_sig = QtCore.Signal(str)
    
    come_out = False
    
    def __init__(self, ipaddress,Folder_path,Totaladd,pingonlyflg,Pingfilehand,engine_inst):
        QtCore.QObject.__init__(self)
        QtCore.QRunnable.__init__(self) 
        self.ipaddress = ipaddress
        self.DupeFlag = "N"
        self.Final_log_path = Folder_path
        self.engine_inst = engine_inst
        
        self.Phase = 1
        self.status = False
        
        self.TotalIP = Totaladd
        self.pingonly = pingonlyflg
        
        self.PingLogfilehand = Pingfilehand
        
        self.pingfileLock = threading.Lock()
        
        self.cancel_sig.connect(self.cancel_action)
        
    def run(self):
      
        if self.engine_inst.quit_flag == True:
                
            self.finishedProcessing.emit(self.TotalIP,self.ipaddress + ": Cancelled")
        
            return 0
        
        
        if (self.pingonly == "True" or self.pingonly == "False") and self.DupeFlag == "N":
            
            status, ping_output = subprocess.getstatusoutput("ping "+ self.ipaddress)
        
            
            self.pingfileLock.acquire()
            self.pingWrite(ping_output)  # this is method where ping file is passed 
            
            if status == 0 :        
                
                
                self.finishedProcessing.emit(self.TotalIP,self.ipaddress + " : Up")
                
            else:
                self.finishedProcessing.emit(self.TotalIP,self.ipaddress + " : Down")
            
            self.pingfileLock.release()
            
            
        
    def pingWrite(self,ping_result):
        
       
        self.PingLogfilehand.write("\n\n==================================================================================\n\n")
            
        self.PingLogfilehand.write("\n")
        self.PingLogfilehand.write(str(self.ipaddress))
        self.PingLogfilehand.write("\n\n")
              
        self.PingLogfilehand.write(ping_result)
        
        self.PingLogfilehand.write("\n\n")
                
            
    def cancel_action(self,message):
        
        self.come_out = True
        
        
        
        
        