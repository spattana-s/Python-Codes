'''
Created on 6 July 2018

@author: sp977u@att.com  (Satish Palnati)

'''

import re
import time
import datetime
import logging

import subprocess
import threading
from threading import Thread, Event
from PySide import QtCore, QtGui

from service_network.device_wheels import devicelogin
from service_network.device_wheels import pushcommandsCiscoRS_ASA
from service_network.device_wheels import pushcommandsJuniper
from service_network.device_wheels import pushcommandsciscoWLC

class CommandProcessor(QtCore.QObject,QtCore.QRunnable):
    
    finishedProcessing = QtCore.Signal(int,int,str)
    
    def __init__(self, ipaddress,progress,usr,pw,Folder_path,UsrCmds,cmdcnt,SingleOut,WLCopt,DupFlag,Totaladd, default_cmd_flag):
        QtCore.QObject.__init__(self)
        QtCore.QRunnable.__init__(self) 
        self.ipaddress = ipaddress
        self.retry = 0
        self.user = usr
        self.pwd = pw
        self.Final_log_path = Folder_path
        self.progress = progress
        self.User_CMD =  UsrCmds
        self.cmdCnt = cmdcnt
        self.Phase = 1
        self.status = False
        self.SingleOutputFile = SingleOut
        self.WLC_opt = WLCopt
        self.DupeFlag = DupFlag
        self.TotalIP = Totaladd
        self.default_cmd_flag = default_cmd_flag
        
        
        #self.pingfileLock = threading.Lock()
        #self.LogFile = logfile
      
    def run(self):
       
        self.loginTrial = devicelogin.Login()
        self.pushcmdCiscoRSASA = pushcommandsCiscoRS_ASA.grindCommands()
        self.pushcmdJuni = pushcommandsJuniper.grindCommands()
        self.pushcmdWLC = pushcommandsciscoWLC.grindCommands()
        
        pingwritelater = "N"
       
       
        try:
            #time.sleep(2)
            if self.DupeFlag =="N":
                self.status = self.Commands_ssh(self.ipaddress,self.user,self.pwd,self.retry,self.SingleOutputFile,self.WLC_opt,self.TotalIP,self.loginTrial)
            #print"\nStatus : "+str(status)
        except Exception as uex :
            print("Something went wrong in Commands ssh Run method ...in phase 1.!")
            print(uex)
            self.status = False
            time.sleep(1)
           
        finally:
            
        
            if self.Phase == 1:
                
                if self.status == True :
                    finished_device_counter = self.progress.updateProgressBar(self.ipaddress,self.Final_log_path,self.status,self.Phase,self.DupeFlag)
                    self.finishedProcessing.emit(self.TotalIP,finished_device_counter,self.ipaddress)
                    self.Phase = 3
                    return 0
                
                elif self.status == False:
                    self.Phase= 2
                
            if self.Phase == 2:
                
                try:
                
                    if self.status == False and self.DupeFlag =="N" :
                        
                        self.retry=0
                        #print " Entered phase 2 and ip : "+str(self.ipaddress)
                        self.status = self.Commands_ssh(self.ipaddress,self.user,self.pwd,self.retry,self.SingleOutputFile,self.WLC_opt,self.TotalIP,self.loginTrial )
                except Exception as uex :
                    print("Something went wrong in Commands ssh Run method ...in phase 2.!")
                    print(uex)
                    self.status = False
                    time.sleep(1)        
                                
                finally:
                    #if self.Phase == 2 and self.DupeFlag =="N":
                        
                    finished_device_counter = self.progress.updateProgressBar(self.ipaddress,self.Final_log_path,self.status,self.Phase,self.DupeFlag)
                    #if self.status == True or self.status == False :
                    self.finishedProcessing.emit(self.TotalIP,finished_device_counter,self.ipaddress)
                            
         
                    #print "\n Phase 2 finally and IP add is : "+str(self.ipaddress)  
            
    def Commands_ssh(self,ipadd,usr,pw,retry,SingleOutputF,WLC,TotalAdd,Logintrial):
        
        self.user = usr
        self.psw = pw
        
        DevType ="NF"
        output = 'x'
        status = False
        session = None
        self.SingleOutputFile = SingleOutputF
        self.matchLock = threading.Lock()
        self.logfileLock = threading.Lock()
        logstat ="F"
        
        IOS_commands  = []
        FW_commands = []
        Juni_commands  = []
        Cisco_Wifi_commands = []
        
        GF = 1
        st = time.asctime( time.localtime(time.time()) )
        DevType= Logintrial.ScreeningDevice(ipadd,usr,pw)
        
        if "SSH negotiation or logical error" in DevType or "un known Error" in DevType :
            
            return False
        
        if DevType == "NF" or DevType == "Unsupported" or "Invalid username or Password" in DevType or "SSH is not enabled" in DevType :
            time.sleep(2)
            DevType= Logintrial.ScreeningDevice(ipadd,usr,pw)
        
        if DevType == "NF" or DevType =="Unsupported" or "SSH negotiation or logical error" in DevType or "Invalid username or Password" in DevType or "un known Error" in DevType:
            
            status = False
            return status
        else:
            
            print( "\nDevice type :  " +DevType +",  IP address :  " +str(ipadd))
        
            if TotalAdd >=48:
                GF= 5
            elif TotalAdd >= 20 and TotalAdd <= 47:
                GF = 4
            elif TotalAdd >= 10 and TotalAdd <= 19:
                GF = 3.6
            else:
                GF= 2.6
                
            if DevType == "NF":
                return False    
            loginstruct = Logintrial.decidePattern(DevType,ipadd,usr,pw,GF)
   
            session,logstat = Logintrial.trylogin(ipadd,**loginstruct)
        
            if logstat =="F":
                time.sleep(1)
                session,logstat = Logintrial.trylogin(ipadd,**loginstruct)
            
        
        if logstat == "F":
            
            return False
            
            
            
        if self.default_cmd_flag == True :
            IOS_commands  = ["show version", "show cdp neighbors","show lldp neighbors","show vlan","show inventory raw","show flash:","show bootflash:","show bootdisk:","show bootvar:","show interfaces status","show interface trunk", "show ip interface brief","show ip ospf summary","show ip bgp summary","show ip bgp neighb","show running"] + self.User_CMD
            FW_commands = ["show version", "show inventory","show flash:","show slot0:","show fail","show route","show arp","show cpu usage","show int brief", "show run access-group","show run nat","show conn count","show running-config","show vpn-sessiondb summary","show crypto isakmp sa","show crypto ipsec sa","show run crypto"] + self.User_CMD
            Juni_commands  = ["show version | no-more", "show system uptime | no-more","show interface terse | no-more","show vlans | no-more","show lldp neighbors | no-more", "show configuration | no-more", "show chassis hardware | no-more","show bgp summary | no-more","show bgp neighbor | no-more","show ospf summary | no-more","show configuration | no-more | display set"] + self.User_CMD
            Cisco_Wifi_commands = ["show sysinfo", "show boot","show run-config commands","show interface summary","show port summary"] + self.User_CMD
        else:
            IOS_commands = self.User_CMD
            FW_commands = self.User_CMD
            Juni_commands = self.User_CMD
            Cisco_Wifi_commands = self.User_CMD
            
        if DevType == "cisco ASA":
            status = self.pushcmdCiscoRSASA.ASA_process(session,ipadd,FW_commands,self.Final_log_path,self.SingleOutputFile,self.matchLock,DevType,self.user,self.psw)
            return status      
        
        if DevType == "cisco":
            
            status = self.pushcmdCiscoRSASA.cisco_RT_SW_process(session, ipadd, IOS_commands,self.Final_log_path,self.SingleOutputFile,self.matchLock,DevType,self.user,self.psw)
               
            return status    
                
        if DevType == "juniper":
            
            status = self.pushcmdJuni.Juniper_process(session, ipadd, Juni_commands, self.Final_log_path,self.SingleOutputFile,self.matchLock,DevType,self.user,self.psw)
            #print("Status :",status)
            #print("IP : ",ipadd)
            return status
        
        elif DevType == "Cisco_Wireless":
            #currently disabled
            return status
            status = self.pushcmdWLC.WLC_process(session, ipadd,Cisco_Wifi_commands, self.Final_log_path,self.SingleOutputFile,self.matchLock,DevType)
            return status                
            
        return status
            