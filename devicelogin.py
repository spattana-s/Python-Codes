
import re
import time
import logging
import netmiko 
import paramiko
#from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException
from netmiko import ConnectHandler
import subprocess
import threading
#import os.path
from threading import Thread, Event
import copy

class Login:

    
    def trylogin(self,ipaddress,**Details):
        
        Stat = "F"
        ver ="NF"
        Temp_session = "NF"
        
        try:
            Stat = 'F'
            st = time.asctime( time.localtime(time.time()) )
            Temp_session = ConnectHandler(**Details)
            time.sleep(0.6)
            pmpt= Temp_session.find_prompt(delay_factor=2)
            
            #ver = Temp_session.send_command_expect("show version")
            en= time.asctime( time.localtime(time.time()) )
            
              
            if '>' in pmpt or '#' in pmpt:
                Stat= 'S'
                
                #print(" LOGGED INTO DEVICE SUCCESS under try login method, ",ipaddress)
                #print(pmpt)
                return Temp_session,Stat
            else:
                
                #print(" LOGGING into device is Failed... , ",ipaddress)
                #print(ver)
                time.sleep(1.5)
                pmpt= Temp_session.find_prompt(delay_factor=2)
                if '>' in pmpt or '#' in pmpt:
                    Stat= 'S'
                    return Temp_session,Stat
                else:
                    Stat = 'F'
                    Temp_session = "NF"
                    return Temp_session,Stat
                    
            #print("start : ",st)
            #print("\n end : ",en)
            return Temp_session,Stat
        
        except (NetMikoAuthenticationException ):
            
            Stat = 'F'
            #print(" LOGGING into device is Failed... under authentication, ",ipaddress)
            Temp_session = "NF"
            time.sleep(2)
            return Temp_session,"F"
                
        except (NetMikoTimeoutException) :
            Stat = 'F'
            #print(" LOGGING into device is Failed...under timeout exec , ",ipaddress)
            Temp_session = "NF"
            time.sleep(2)
            return Temp_session,"F"
        except Exception as ex:
            Stat = 'F'
            #print(" LOGGING into device is Failed...under generic exception , ",ipaddress)
            print(ex)
            Temp_session = "NF"
            return Temp_session,Stat
        
    def ScreeningDevice(self,ipadd,usr,pw):    
        devType ="NF"
        try:
                
            remote= paramiko.SSHClient()
            remote.load_system_host_keys()
            remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            remote.connect(ipadd,username = usr, password = pw)
            #paramiko.util.log_to_file("ATTBACKUP.log")
            time.sleep(0.6)
            my_conn = remote.invoke_shell()
            my_conn.settimeout(None)
            time.sleep(0.5)
            
            my_conn.send("\n\r")
            
            time.sleep(1)
            my_conn.send("show version\n\r")
            
            time.sleep(1)
            
            res = my_conn.recv(65534).decode('utf-8', 'ignore')
            
            while 1:
                if  my_conn.recv_ready():
                    res += my_conn.recv(65534).decode('utf-8', 'ignore')
                    time.sleep(0.2)
                else:
                    break  
 
            ver = str(res)
            
            devType = self.getType(ver,ipadd)
            #ver = ver.encode('utf-8')
            #print(ver)
              
            remote.close()
            
            return devType
            
                
        except paramiko.AuthenticationException:
            #print ("Invalid Username or Password....!",ipadd)
            time.sleep(2)
            return "Invalid username or Password"
             
        except paramiko.ssh_exception.NoValidConnectionsError:
            print ("unable to make SSH ...!    " +ipadd)
            return "NF"
            
        except subprocess.CalledProcessError:
            print ("Device  is not reachable ,  Please check and fix ...! "+ipadd)
            return "NF"
            
        except paramiko.ssh_exception.SSHException as ue :
            print ("SSH negotiation or logical error,  retrying .... !  " +ipadd)
            return "SSH negotiation or logical error"
        except Exception as ue:
            print("Unknown exception occured ....!",ue)
            time.sleep(1)
            return "un known Error"
            
            
    def getType(self,ver,ip):
        Type = "NF"
        
        if re.search(r"ASA", ver)  or re.search(r"Adaptive", ver) or "Adaptive" in ver or  "ASA" in ver :
            Type = "cisco ASA"
        
        elif re.search(r"Cisco wireless", ver)  or re.search(r"Lan Controller", ver) or "Cisco Controller" in ver or "WLC" in ver or "Controller"  in ver :
            Type = "Cisco_Wireless"   
        elif re.search(r"junos", ver)  or re.search(r"JUNOS", ver) or re.search(r"juniper", ver) or re.search(r"Juniper", ver) or "juniper" in ver  or "JUNO" in ver:
            Type = "juniper" 

        elif re.search(r"Cisco IOS", ver) or re.search(r"Cisco", ver)  or re.search(r"IOS", ver) or re.search(r"cisco", ver) or  "Cisco IOS" in ver or "Cisco" in ver or "IOS" in ver or "AIR-AP1242" in ver or re.search(r"AIR-AP1242", ver) :
            Type = "cisco"  
            
        else:
            Type ="NF"
            print("\n Could not Fetch type..!  :  " ,ip)
          
        return Type
    def decidePattern(self,DevType,ipadd,usr,pw,GF):
        
        
        if "cisco ASA" in DevType :
            Cisco_FW = { 'device_type': 'cisco_asa' , 'ip' : ipadd, 'username' : usr ,'password' : pw, 'secret' : pw, 'global_delay_factor' : GF , }
            return Cisco_FW
        elif "cisco" == DevType :
            Cisco_RS= { 'device_type': 'cisco_ios' , 'ip' : ipadd, 'username' : usr ,'password' : pw, 'secret' : pw, 'global_delay_factor' : GF, }
            return Cisco_RS
        elif "juniper" in DevType :
            Juno = {'device_type': 'juniper_junos' , 'ip' : ipadd , 'username' : usr ,'password' : pw, 'global_delay_factor' : GF ,   }
            return Juno
        elif "Cisco_Wireless" in DevType :
            C_WLAN = { 'device_type': 'cisco_wlc' , 'ip' : ipadd, 'username' : usr ,'password' : pw, 'global_delay_factor' : 4 , }
            return C_WLAN
        else:
            return "NF"
            
        
   
            

            
                
    '''excepName = type(e).__name__
                print ("SSH negotiation or logical error,  retrying .... !  " +ipadd)
                self.logfileLock.acquire()
                logfile = open(self.LogFile,"a+")
                logfile.write("================================================\n")
                logfile.write(str(ipadd))
                
                logfile.write("\nSSH negotiation or logical error\n")
                logfile.write(str(excepName))
                
                logfile.write("\n================================================\n" )
                logfile.close()
                self.logfileLock.release() 
    
                
            

        
        


import netmiko

import devicelogin

ipadd = "9.118.104.7"

det= { 'device_type': 'cisco_ios' , 'ip' : ipadd, 'username' : "sp977u" ,'password' : "Cheta$56", 'secret' : "Cheta$56",'global_delay_factor' : 2 ,}

log =devicelogin.Login()

session,stat= log.trylogin(ipadd,**det)

session.disconnect()


9.109.71.7
9.96.255.109  '''