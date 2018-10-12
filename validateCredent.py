'''
Created on May 2, 2017

@author: sp977u

'''
from PySide import QtCore,QtGui

import sys
from service_network.device_wheels import devicelogin
import time

class validateCredent(QtCore.QObject,QtCore.QRunnable) :
    
    validate_signl = QtCore.Signal(str,str) #dev type , cred test 
    
    def __init__(self,IPList,usr,pw):
        QtCore.QObject.__init__(self)
        QtCore.QRunnable.__init__(self) 
        
        self.IPList = IPList
        self.usr = usr
        self.pw = pw
        
    def run(self):
    
    #def checkCredentials(self,IPList,usr,pw):

        trialcount = 0
        Devtype = 'NF'
        badUsernamePass = 0
        job_done = "No"
        credtestpass = "Fail"
        
        scan = devicelogin.Login()
        
        '''for item in range(len(IPList)):
            ip =  str(IPList[item])
            ip = ip.strip('[').strip(']').strip("'")
            IPList[item] = ip'''
    
        try :
            
        
            for ipadd in self.IPList:
                
                print(ipadd)
            
                Devtype = scan.ScreeningDevice(ipadd, self.usr, self.pw)
                #loc = loc + 1
                trialcount = trialcount + 1
            
            
                if "SSH is not enabled" in Devtype or "SSH negotiation or logical error" in Devtype or "un known Error" in Devtype or "Device  is not reachable" in Devtype :
                    continue
                if "Invalid username or Password" in Devtype :
                    badUsernamePass += 1
                    if badUsernamePass >= 2 :
                        Devtype = "Invalid username or Password"
                        break
                    continue
                if "cisco ASA" in Devtype or "cisco" in Devtype or "juniper" in Devtype or "Cisco_Wireless" in Devtype:
                    #print("Credentials check passed...!")
                    credtestpass = "Passed"
                    job_done = "Yes"
                    self.validate_signl.emit(Devtype,credtestpass)
                    break
                #if loc >= len(IPList):
                #    break
        
            if credtestpass == "Fail" :
                self.validate_signl.emit(Devtype,credtestpass)
    
    
        except Exception as ex:
            print(ex)
            credtestpass = "Fail"
            self.validate_signl.emit(Devtype,credtestpass)
#             return 0
            #return Devtype, credtestpass
        
            # log this 
            
        
            
        
                
        