import os
import re
import copy
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import time
import ipcalc
from service_network.device_wheels import captures
from service_network.device_wheels import devicelogin

import logging

from netaddr import IPNetwork


class grindCommands:
    
    def __init__(self):
        
        self.loginTrial = devicelogin.Login()
        self.user = ""
        self.psw = ""
    
    def ASA_process(self,session,ipadd,FW_commands,Final_log_path,SingleOutputFile,matchLock,devtype,usr,pw):
        
        self.user = usr
        self.psw = pw
        self.capASA = captures.outPutcaptures()
        command_type = "NF"
        status = False
        pmpt = "NF"          
        try:
            session.enable()
            time.sleep(1)
            pmpt = session.find_prompt(delay_factor=2)
            
            if "vfw" in pmpt or "VFW" in pmpt :
                res = session.send_command("changeto context system",strip_prompt=False)
                time.sleep(0.5)
                pmpt = session.find_prompt(delay_factor=2)
            
        except AttributeError as ex: 
            print(ex)
            Enable_Status = 'F'
            #print ("Problem in logging to ASA  enable mode  : "+str(ipadd))
            status = False
            return status
            
        except ValueError as ex:
            print(ex)                      
            Enable_Status = 'F'
            #print ("Problem in logging to ASA  enable mode  : "+str(ipadd))
            return False
        except Exception as ex:
            print(ex)
            #print ("Problem in logging to ASA enable mode with generic exc : "+str(ipadd))
            
            return False
            
        ipfile = Final_log_path  +  str(ipadd) + ".txt"
                            
        myfile=  open(ipfile,"w")
                        
                               
        hostnm = copy.copy(pmpt)
        hostnm = hostnm[:-1]
        pmpt_sh = pmpt
                        
        myfile.write("Hostname : " + hostnm)
        myfile.write("\n")
        myfile.write("IP address : " + ipadd )
        
        myfile.write("\n\n")
        myfile.write(pmpt)
        myfile.write("\n")
        myfile.write(pmpt)
        
        
        for cmd in FW_commands:
                  
            cmd = str(cmd).strip("[").strip("]").strip("'").strip()     
            Flag = 'F'    
            
            if ("_Juniper" in cmd or "_Cisco" in cmd or "VG224" in cmd)  and devtype == "cisco ASA":
                continue
            if "_ASA" in cmd or "_General" in cmd:
                cmd = cmd [ : cmd.rfind("_") -1 ]
            
            time.sleep(0.3) 
            
            if cmd.startswith("show") or cmd.startswith("sho") or cmd.startswith("sh "):
                command_type = "show"
                if session.check_config_mode() :
                    myfile.write("\n")
                    myfile.write(pmpt)
                    myfile.write("exit")
                    session.exit_config_mode()
                    pmpt = pmpt_sh   
                    
                    myfile.write("\n")
                result,Cap_Cnt,Flag = self.capASA.CaptureOutput(session,cmd,0,Flag,pmpt)
                    
            else:
                command_type = "config"
                myfile.write("\n")
                myfile.write(pmpt )
                myfile.write(cmd)
                myfile.write("\n")
                    
                result,Cap_Cnt,Flag,pmpt = self.capASA.RunOtherCommands(session,cmd,0,Flag,myfile)
             
                pmpt = session.find_prompt(delay_factor=2)
                myfile.write("\n")
                
                    
            if Flag == 'S' :
                time.sleep(0.1)    
                if len(result )>= 10 and "syntax error" not in result and "Invalid" not in result : 
                    myfile.write("\n")
                    
                    myfile.write(pmpt)
                    myfile.write(cmd)
                    myfile.write("\n")    
                    myfile.write(result)
                             
            elif Flag == 'F' and command_type == "show":
                Cap_Cnt = Cap_Cnt + 1
                result,Cap_Cnt,Flag = self.capASA.CaptureOutput(session,cmd,0,Flag,pmpt)
                
            if Cap_Cnt > 4 or Flag == "F" :
                        
                session.disconnect()
                myfile.close
                try :
                    
                    os.remove(ipfile)
                except PermissionError :
                    time.sleep(2)
                    myfile.close()
                    os.remove(ipfile)
                finally:    
                    return False
                
            myfile.write("\n")
            myfile.write(pmpt)
            myfile.write("\n")
            myfile.write("\n\n")
            
               
        myfile.write(pmpt)
        myfile.write("\n")
        myfile.write("\n")
                
        session.disconnect()
        myfile.close() 
        status = True
        if status == True and SingleOutputFile == "True":
            
            flatstat = self.capASA.writeFlatfile(ipfile,ipadd,pmpt,Final_log_path)
            
        return status
    
    # =========================================   End of  ASA section  ========================================
    
    def cisco_RT_SW_process(self,session,ipadd,IOS_commands,Final_log_path,SingleOutputFile,matchLock,devtype,usr,pw):
        
        pmpt = "NF"
        status = False
        Cap_Cnt = 0
        realcmd = "NF"
        parentDevtype = "NF"
        self.user = usr
        self.psw = pw
        self.capCiscoRS = captures.outPutcaptures()
        subnets_capture = "No"
        command_type = 'NF'
        child_vlans_output = " "
        
        logfile_closed = "No"       
        try:
            session.enable()
            time.sleep(1)
            pmpt = session.find_prompt(delay_factor=2)
            
            if ">" in pmpt or "#" in pmpt:
                pass
            else:
                time.sleep(1)
                session.enable()
                time.sleep(1)
                pmpt = session.find_prompt(delay_factor=3)
        
        except AttributeError:
            #print ("Problem in logging to Cisco RS  enable mode  : "+str(ipadd))
            return False    
        except ValueError:                      
            
            #print ("Problem in logging to Cisco RS  enable mode  : "+str(ipadd))    
            return False
                  
        except Exception as uex:
            #print ("Problem in logging to Cisco RS  enable mode with generic exce : "+str(ipadd))    
            print("Gen exception in getting to get enable  ...")
            return False
               
        ipfile = Final_log_path +   str(ipadd) + ".txt"
               
        myfile=  open(ipfile,"w")
        
        hostnm = copy.copy(pmpt)                  
        hostnm = hostnm[:-1]
        
        pmpt_sh = pmpt
        myfile.write("Hostname : " + hostnm)
        myfile.write("\n")
        myfile.write("IP address : " + ipadd )
    
        myfile.write("\n\n\n")
        
        myfile.write(pmpt)
        myfile.write("\n")
        myfile.write(pmpt)
            
        for cmd in IOS_commands:
            if "show run vlan _Cisco" in cmd:
                realcmd = cmd[:]
                       
            cmd = str(cmd).strip("[").strip("]").strip("'").strip()   
            Flag = 'F'    
            
                
            if ( "_Juniper" in cmd or "_ASA" in cmd ) and devtype == "cisco":
                continue
            if  "_VG224" in cmd  and devtype == "cisco":
                cmd = cmd [ : cmd.rfind("_") -1 ]
            if "_Cisco" in cmd or "_General" in cmd:
                cmd = cmd [ : cmd.rfind("_") -1 ]
        
            time.sleep(0.2)
            
            if cmd.startswith("show") or cmd.startswith("sho") or cmd.startswith("sh "):
                command_type = "show"  
                if session.check_config_mode():
                    myfile.write("\n")
                    myfile.write(pmpt)
                    myfile.write("exit")
                    session.exit_config_mode()
                    pmpt = pmpt_sh   
                    myfile.write("\n")
                    
                result,Cap_Cnt,Flag = self.capCiscoRS.CaptureOutput(session,cmd,0,Flag,pmpt)
                
                #print("Cap count value : ",Cap_Cnt, " Flag is  :",Flag ,"For ip add : ",ipadd)
                
                if "show run | in ip route 0.0.0.0 _Cisco" in realcmd :
                    self.get_parent_device(session, pmpt, myfile)
                
                if "show run vlan _Cisco" in realcmd  and Flag == "S": # block for handling vlans and subnets capturing
                    
                    subnets_capture = "Yes"
                    child_vlans_output = result[:]
                    
                    self.get_vlans_info(result,myfile)
                    parent_device_found = "No"
                    # we will first try to check if there are local L3 with subnets configured
                    self.scan_subnet_details_local(session,pmpt,myfile)
                    
                    if len(self.vlan_all) != self.local_vlans_found :
                        Flag = "F"
                        result,Cap_Cnt,Flag = self.capCiscoRS.CaptureOutput(session,"show run | in ip route 0.0.0.0 ",0,Flag,pmpt)
                        parent_device_found = "No"
                        
                        myfile.write("\n" + result + "\n\n")
                        
                        result = result.split("\n")
                        for item in result:
                        
                            if "ip route 0.0.0.0 0.0.0.0" in item:
                                item = item.replace("ip route 0.0.0.0 0.0.0.0 ", '')
                                ipPat = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
                                parent_ip = re.findall(ipPat, item )
                                parent_ip = str(parent_ip[0]).strip()
                                parent_device_found = "Yes"
                                myfile.write("\n\n  Parent IP : " + parent_ip +"\n")
                                break
                        
                        if parent_device_found == "No":
                            Flag = "F"
                            result,Cap_Cnt,Flag = self.capCiscoRS.CaptureOutput(session,"show run | in ip default-gateway ",0,Flag,pmpt)
                            myfile.write("\n" + result + "\n\n")
                            result = result.split("\n")
                            
                            for item in result:
                                if "ip default-gateway " in item:
                                    item= item.strip()
                                    parent_ip = item.replace("ip default-gateway ",'').strip()
                                    parent_device_found = "Yes"
                                    myfile.write("\n\n  Parent IP : " + parent_ip +"\n")
                                    
                                    
                                    break
                                    
                                    #print("parent ip in default gateway : ",parent_ip)
                                    
                        if parent_device_found == "Yes" :
                            
                            parent_type_found = "No"
                            
                            parentDevtype = self.loginTrial.ScreeningDevice(parent_ip,self.user ,self.psw)
                            time.sleep(1)
                            if parentDevtype == "Invalid username or Password" or parentDevtype == "NF" or parentDevtype == "SSH negotiation or logical error" or parentDevtype == "un known Error" :
                                time.sleep(1)
                                parentDevtype = self.loginTrial.ScreeningDevice(parent_ip,self.user ,self.psw)
                                time.sleep(1)
                            if parentDevtype == "Invalid username or Password" or parentDevtype == "NF" or parentDevtype == "SSH negotiation or logical error" or parentDevtype == "un known Error" :
                                print("Unable to login Parent device : ",parent_ip)
                                parent_type_found = "No"
                            #print("Parent dev type : " ,parentDevtype, " parent ip is  :", parent_ip ,ipadd)
                            self.write_vlans_from_parent(parent_ip,parentDevtype,myfile)
                           
                    myfile.write("\n\n")        
                    result = child_vlans_output[:]
                    
                    
            else:
                command_type = "config"
                myfile.write("\n")
                myfile.write(pmpt)
                myfile.write(cmd)
                myfile.write("\n")
                    
                result,Cap_Cnt,Flag,pmpt = self.capCiscoRS.RunOtherCommands(session,cmd,0,Flag,myfile)
                    
                             
            if Flag == 'S' and command_type == "show":
                  
                if len(result )>= 10 and "syntax error" not in result and "Invalid" not in result :
                    myfile.write("\n")    
                    myfile.write(pmpt)
                    myfile.write(cmd)
                    myfile.write("\n")
                    myfile.write(result)
            elif Flag == 'F' and command_type == "show":
                Cap_Cnt = Cap_Cnt + 1
                result,Cap_Cnt,Flag = self.capCiscoRS.CaptureOutput(session,cmd,0,Flag,pmpt)
                
                   
            if Cap_Cnt > 4 or Flag == "F" :
                        
                session.disconnect()
                myfile.close
                try :
                    
                    os.remove(ipfile)
                except PermissionError :
                    time.sleep(2)
                    myfile.close()
                    os.remove(ipfile)
                finally:    
                    return False
                  
            myfile.write("\n")
            myfile.write(pmpt)
            myfile.write("\n")
            myfile.write("\n")
             
            
        myfile.write(pmpt)
        myfile.write("\n\n\n")
                  
        session.disconnect()
        myfile.close()
        status = True
        
        '''# writing seperate section for subnets handling from parent device
        if "show run vlan _Cisco" in realcmd and subnets_capture == "Yes" :
            if parent_device_found == "Yes" :
                                    
                parentDevtype = self.loginTrial.ScreeningDevice(parent_ip,self.user ,self.psw)
                time.sleep(3)
                if parentDevtype == "Invalid username or Password" or parentDevtype == "NF" or parentDevtype == "SSH negotiation or logical error" or parentDevtype == "un known Error" :
                    time.sleep(3)
                    parentDevtype = self.loginTrial.ScreeningDevice(parent_ip,self.user ,self.psw)
                    time.sleep(3)
                if parentDevtype == "Invalid username or Password" or parentDevtype == "NF" or parentDevtype == "SSH negotiation or logical error" or parentDevtype == "un known Error" :
                    print("Unable to login Parent device : ",parent_ip)
                    parent_type_found = "No"
                print("Parent dev type : " ,parentDevtype, " parent ip is  :", parent_ip ,ipadd)
                
                if parentDevtype != "NF" :
                    
                    self.write_vlans_from_parent(parent_ip,parentDevtype,myfile)
            
        # closing log file handle finally   
        myfile.write("\n\n\n")
        myfile.write(child_vlans_output)
        myfile.write("\n\n")  '''
         
    
        if status == True and SingleOutputFile == "True":
                
            flatstat = self.capCiscoRS.writeFlatfile(ipfile,ipadd,pmpt,Final_log_path)
                
        return status
    
    def get_vlans_info(self,output,filehand):
        
        self.output =  output.split('\n')
        self.vlan_all = []
    
        for cmd in self.output:
            
            if cmd.lower().strip().startswith("vlan 1" ) or cmd.lower().strip().startswith("vlan 2" ) or cmd.lower().strip().startswith("vlan 3" ) or cmd.lower().strip().startswith("vlan 4" ):
                
                self.VLAN = self.decide_vlan_number(cmd)
                
                if self.VLAN >= 100 :
                    self.vlan_all.append(self.VLAN)
                
                if self.VLAN >= 1901 and self.VLAN <= 1999 :
                    filehand.write("\n\n MGMT VLAN: " + str(self.VLAN)+"\n")  #  when MGMT 
                elif (self.VLAN >= 2001 and self.VLAN <= 2020 ) or ( self.VLAN >= 3001 and self.VLAN <= 3020) or (self.VLAN >= 2501 and self.VLAN <= 2520) or (self.VLAN >= 3501 and self.VLAN <= 3503):
                    filehand.write("\nDATA VLAN (blue-1): " + str(self.VLAN)+"\n")  #  when v = 0
            
                elif (self.VLAN >= 2021 and self.VLAN <= 2040) or (self.VLAN >= 3021 and self.VLAN <= 3040) or (self.VLAN >= 2501 and self.VLAN <= 2520) or (self.VLAN >= 3521 and self.VLAN <= 3523):
                    filehand.write("\nDATA VLAN (blue-2): " + str(self.VLAN)+"\n") # when v = 1
                    
                elif (self.VLAN >= 2041 and self.VLAN <= 2060) or (self.VLAN >= 3041 and self.VLAN <= 3060) or (self.VLAN >= 2541 and self.VLAN <= 2560 ) or (self.VLAN >= 3541 and self.VLAN <= 3543 ) :
                    filehand.write("\nVOICE VLAN (blue-3): " + str(self.VLAN)+"\n")  # when v = 2
                    
                elif (self.VLAN >= 2061 and self.VLAN <= 2080) or (self.VLAN >= 3061 and self.VLAN <= 3080 ) or (self.VLAN >= 2561 and self.VLAN <= 2580 ) or (self.VLAN >= 3561 and self.VLAN <= 3563 ) : 
                    filehand.write("\nVOICE VLAN (blue-4): " + str(self.VLAN)+"\n")  # when v = 3
                    
                elif ( self.VLAN >= 2101 and self.VLAN <= 2120 ) or (self.VLAN >= 3101 and self.VLAN <= 3120) or (self.VLAN >= 2601 and self.VLAN <= 2620) or (self.VLAN >= 3601 and self.VLAN <= 3603) or (self.VLAN >= 2121 and self.VLAN <= 2140 ) or (self.VLAN >= 3121 and self.VLAN <= 3140) or (self.VLAN >= 2621  and self.VLAN <= 2640) or (self.VLAN >= 3621 and self.VLAN <= 3623) or (self.VLAN >= 2141 and self.VLAN <= 2160) or (self.VLAN >= 3141 and self.VLAN <= 3160) or (self.VLAN >= 2641 and self.VLAN <= 2660) or (self.VLAN >= 3641 and self.VLAN <= 3643) or (self.VLAN >= 2161 and self.VLAN <= 2180) or (self.VLAN >= 3161 and self.VLAN <= 3180) or (self.VLAN >= 2661 and self.VLAN <= 2680) or (self.VLAN >= 3661 and self.VLAN <= 3663) or (self.VLAN >= 2181 and self.VLAN <= 2200) or (self.VLAN >= 3181 and self.VLAN <= 3200 ) or (self.VLAN >= 2681 and self.VLAN <= 2700 ) or (self.VLAN >= 3681 and self.VLAN <= 3683 ) :
                    filehand.write("\nBLUE WIRELESS VLAN (blue-5 to 9): " + str(self.VLAN)+"\n")  # when v= 5-9
                    
                elif (self.VLAN >= 2301 and self.VLAN <= 2320) or (self.VLAN >= 3301 and self.VLAN <= 3320) or (self.VLAN >= 2801 and self.VLAN <= 2820) or (self.VLAN >= 3801 and self.VLAN <= 3803) or (self.VLAN >= 2321 and self.VLAN <= 2340 ) or (self.VLAN >= 3321 and self.VLAN <= 3340) or (self.VLAN >= 2821 and self.VLAN <= 2840) or (self.VLAN >= 3821 and self.VLAN <= 3823 ):
                    filehand.write("\nGUEST WIRELESS VLAN (blue-15 to 16): " + str(self.VLAN)+"\n") # when  v = 15 - 16
                    
                elif (self.VLAN >= 2301 and self.VLAN <= 2320) or (self.VLAN >= 3301 and self.VLAN <= 3320) or (self.VLAN >= 2801 and self.VLAN <= 2820) or (self.VLAN >= 3801 and self.VLAN <= 3803) or (self.VLAN >= 2321 and self.VLAN <= 2340) or (self.VLAN >= 3321 and self.VLAN <= 3340) or (self.VLAN >= 2821 and self.VLAN <= 2840) or (self.VLAN >= 3821 and self.VLAN <= 3823) or (self.VLAN >= 2341 and self.VLAN <= 2360) or (self.VLAN >= 3341 and self.VLAN <= 3360) or (self.VLAN >= 2841 and self.VLAN <= 2860 ) or (self.VLAN >= 3841 and self.VLAN <= 3843) or (self.VLAN >= 2361 and self.VLAN <= 2380) or (self.VLAN >= 3361 and self.VLAN <= 3380) or (self.VLAN >= 2861 and self.VLAN <= 2880) or (self.VLAN >= 3861 and self.VLAN <= 3863 ) or (self.VLAN >= 2381 and self.VLAN <= 2400 ) or (self.VLAN >= 3361 and self.VLAN <= 3380) or (self.VLAN >= 3301 and self.VLAN <= 3320) or (self.VLAN >= 2881 and self.VLAN <= 2900) or (self.VLAN >= 3881 and self.VLAN <= 3883 ):
                    filehand.write("\nYELLOW WIRELESS VLAN (blue-15 to 19): " + str(self.VLAN)+"\n")  # when v = 15 - 19
                    
                elif (self.VLAN >= 2481 and self.VLAN <= 2500) or (self.VLAN >= 3481 and self.VLAN <= 3500) or (self.VLAN >= 2981 and self.VLAN <= 3000 ) or (self.VLAN >= 3981 and self.VLAN <= 3983):
                    filehand.write("\nsingle WLC global MGMT VLAN (v-24): " + str(self.VLAN)+"\n")  # when  = 24
                    
                elif "4022" in str(self.VLAN) :
                    filehand.write("\nsingle WLC Transport VLAN :   " + str(self.VLAN)+"\n")
                elif "4023" in str(self.VLAN) :
                    filehand.write("\nsingle WLC VE Transport VLAN :   " + str(self.VLAN)+"\n")
                elif "4051" in str(self.VLAN) :
                    filehand.write("\nsingle WLC HREAP VLAN :   " + str(self.VLAN)+"\n")
                elif "4094" in str(self.VLAN):
                    filehand.write("\nNULL VLAN 4094 Status :   " + str(self.VLAN)+"\n")
                else:
                    filehand.write("\nMisc / Non Standard VLAN : " + str(self.VLAN)+"\n")   
                
    def decide_vlan_number(self,line):
    
        try :
            vlanformat =    re.compile(r'\d\d\d\d')
            vlan_num = vlanformat.search(line)
            if vlan_num == None:  # if we face issue with data and can not find match , we handle like this , where None object can  not be returned to caller.
                return 0
            
            vlan_num = int(vlan_num.group())
            return vlan_num
        except Exception as ex :
            print(ex)
            print("There is something wrong for VLAN number identification in pushcommands module cisco RS ..., Please check with admin...")
            #self.headTrim.GUI.msgBox.critical(self.headTrim.GUI,'Error!',"There is something wrong with File operation..., Please check file sources...!",self.headTrim.GUI.QtGui.QMessageBox.Ok)
            return 0
            
    def scan_subnet_details_local(self,session,pmpt,filehand):
        Flag = "F"
        Cap_Cnt =0
        self.local_vlans_found = 0
        ipPat = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        network_with_cidr = "NF"
        local_subnet_found = "No"
        for vl in self.vlan_all:
            Flag = "F"
            result,Cap_Cnt,Flag = self.capCiscoRS.CaptureOutput(session,"show run interface vlan" +str(vl) ,0,Flag,pmpt)
            local_subnet_found ="No"
            if "ip address " in result:
                result = result.split('\n') 
            
            
            for item in result:
                if "no ip address " in item.lower():
                    local_subnet_found = "No"
                    break
                if "ip address " in item and "." in item:
                    ip_address_with_mask  = re.findall(ipPat,item)
                    
                    addr = ipcalc.IP(ip_address_with_mask[0], mask= ip_address_with_mask[1])
                    network_with_cidr = str(addr.guess_network())
                    local_subnet_found = "Yes"
                    filehand.write( "\n" + str(vl) + " Subnet : " + network_with_cidr + '\n')
                    
                    self.local_vlans_found += 1
                    break
            if local_subnet_found == "No" :
                Flag = "F"
                result,Cap_Cnt,Flag = self.capCiscoRS.CaptureOutput(session,"show interface vlan" +str(vl) ,0,Flag,pmpt)
                local_subnet_found ="No"
                result = result.split('\n')
                for item in result:
                    
                    if "Internet address is" in item and "." in item:
                        
                        final_subnet = item.replace("Internet address is", '').strip()
                        ip = IPNetwork(final_subnet )
                        final_subnet = str(ip.cidr)
                            
                        local_subnet_found = "Yes"
                        filehand.write( "\n" + str(vl) + " Subnet : " + final_subnet + '\n')
                        
                        self.local_vlans_found += 1
                        break
                    
            
                        
    def write_vlans_from_parent(self,parent_ip,parent_dev_type,filehandle):
        
        GF = 4
        logstat = False
        localcmd = "NF"
        parent_pmpt = "NF"
        realsyntax = ' '
        parent_session = None
        patternfound = "No"
        loginstruct_trails = 0
        session_trials = 0
        prompt_trials = 0
        try :
            '''# pattern prep ; 5 trails
            while loginstruct_trails <= 5:
                loginstruct = self.loginTrial.decidePattern(parent_dev_type,parent_ip,self.user ,self.psw ,GF) 
                
                if loginstruct_trails == 5:
                    print("Unable to decide pattern for ",parent_ip)
                    
                    break
                if len(loginstruct) >= 3:
                    patternfound = "Yes"
                    print("Login struct found in ",loginstruct_trails ," Trials for device : ",parent_ip)
                    break
                loginstruct_trails += 1
                time.sleep(0.3)  '''
                
            if "cisco ASA" in parent_dev_type :
                loginstruct = { 'device_type': 'cisco_asa' , 'ip' : parent_ip, 'username' : self.user ,'password' : self.psw, 'secret' : self.psw , 'global_delay_factor' : GF , }
            
            elif "cisco" == parent_dev_type :
                loginstruct= { 'device_type': 'cisco_ios' , 'ip' : parent_ip, 'username' : self.user  ,'password' : self.psw , 'secret' : self.psw, 'global_delay_factor' : GF, }
            
            elif "juniper" in parent_dev_type :
                loginstruct = {'device_type': 'juniper_junos' , 'ip' : parent_ip , 'username' : self.user ,'password' : self.psw, 'global_delay_factor' : GF ,   }
            
            elif "Cisco_Wireless" in parent_dev_type :
                loginstruct = { 'device_type': 'cisco_wlc' , 'ip' : parent_ip, 'username' : self.user ,'password' : self.psw , 'global_delay_factor' : 4 , }
            else:
                loginstruct = "NF"
    
            
            # session prep : 5 trials
            while session_trials <= 5:
                if type(loginstruct) == str:
                    parent_session = None
                    break
                parent_session,logstat = self.loginTrial.trylogin(parent_ip,**loginstruct)
                
                if logstat == "S" or session_trials == 5:
                    break
                if logstat== "F" or type(parent_session) == str:
                    parent_session = None
                    time.sleep(3)
                    
                session_trials += 1
            
            #print("after login trails Parent ip : ",parent_ip ,parent_session,logstat)        
            
            if type(parent_session) == str:
                return 0
            
            
            '''loginstruct = self.loginTrial.decidePattern(parent_dev_type,parent_ip,self.user ,self.psw ,GF)    
            
            if loginstruct == None:
                loginstruct = self.loginTrial.decidePattern(parent_dev_type,parent_ip,self.user ,self.psw ,GF)
            
            
            
            if loginstruct != None:
                time.sleep(2)
                parent_session,logstat = self.loginTrial.trylogin(parent_ip,**loginstruct) # trail 1
        
    
            if logstat =="F":
                time.sleep(2)
                loginstruct = self.loginTrial.decidePattern(parent_dev_type,parent_ip,self.user ,self.psw ,GF)
                if loginstruct == None:
                    loginstruct = self.loginTrial.decidePattern(parent_dev_type,parent_ip,self.user ,self.psw ,GF)
                time.sleep(3)
                parent_session,logstat = self.loginTrial.trylogin(parent_ip,**loginstruct)  # trail  2  '''
            
            
            if parent_dev_type == "cisco":
                realsyntax = "show interface vlan "
            if parent_dev_type == "juniper" :
                realsyntax = "show interfaces terse | match irb."
                
            # parent prompt trials = 5
            while prompt_trials <= 5:
                if parent_session == None :
                    break
                
                if parent_session != None and parent_dev_type == "cisco" and type(parent_session ) != str:
                    parent_session.enable()
                    time.sleep(1)
                    #parent_pmpt = parent_session.find_prompt(delay_factor=3)
                
                parent_pmpt = parent_session.find_prompt()
                    
                    #print("current prompt for ip : ",parent_pmpt,parent_ip)
                if (">"  in parent_pmpt and "juniper" in parent_dev_type ) or ( "#"  in parent_pmpt and "cisco" in parent_dev_type ) or prompt_trials == 5 or type(parent_session) == str:
                    #print("Prompt trails for parent ip : ",prompt_trials,parent_ip)
                    break
                time.sleep(2)
                prompt_trials += 1
                
            
            '''if parent_session != None and parent_dev_type == "cisco":
                parent_session.enable()
                time.sleep(1)
                
            if parent_session != None :    
                parent_pmpt = parent_session.find_prompt()
                
            if ">"  in parent_pmpt or "#"  in parent_pmpt :
                pass
            else:
                if parent_session != None and parent_dev_type == "cisco":
                    parent_session.enable()
                time.sleep(2)
                if parent_session != None :  
                    parent_pmpt = parent_session.find_prompt()
                    time.sleep(1)
                if ">"  in parent_pmpt or "#"  in parent_pmpt :
                    pass
                else:
                    parent_pmpt = "NF"   '''
                
            #print("Parent prompt for ",parent_ip,parent_pmpt)
            if parent_pmpt == "NF" or type(parent_session) == str or parent_session == None:
                print(parent_session)
                return 0
        
            if parent_pmpt != "NF" and parent_session != None and type(parent_session) != str:
                
                #print("Successfully logged in for final vlan on parent : ",parent_ip,parent_pmpt)
                
                for vlan in self.vlan_all:
                    if "4094" in str(vlan):
                        continue
                    Flag = "F" # sending local vlan command to parent to get SVI info
                    localcmd = (realsyntax  + str(vlan)).strip()
                    
                    result,Cap_Cnt,Flag = self.capCiscoRS.CaptureOutput(parent_session,localcmd  ,0,Flag,parent_pmpt)
                    
                    result = result.split("\n" )
                    #print("Result for parent ip is  : ",parent_ip,result)
                    final_subnet = " "
                    for item in result :
                        if  str(vlan) in item and "up" in item and "." in item and "/" in item: 
                            item = item.strip()
                            final_subnet = item[ item.rfind(" ") :].strip()
                            
                            filehandle.write("\n " + str(vlan) + " Subnet : " + final_subnet)
                            break
                            
                        if "Internet address is" in item and parent_dev_type == "cisco":
                            final_subnet = item.replace("Internet address is", '').strip()
                            ip = IPNetwork(final_subnet )
                            final_subnet = str(ip.cidr)
                            
                            filehandle.write("\n " + str(vlan) + " Subnet : " + final_subnet)
                            break
                    #print("Final subnet : ",final_subnet,parent_ip)
                                    
                parent_session.disconnect()
                
        except Exception as ex:
            print(" There is something wrong in get vlans from parent method in pushcommands RS-ASA class")
            print(ex)
            
    def get_parent_device(self,session,pmpt,filehand):
        
        Flag = "F"
        parent_device_found = "No"
        ipPat = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        
            
        result,Cap_Cnt,Flag = self.capCiscoRS.CaptureOutput(session,"show run | in ip route 0.0.0.0 ",0,Flag,pmpt)
        parent_device_found = "No"
        result = result.split("\n")
        for item in result:
        
            if "ip route 0.0.0.0 0.0.0.0 " in item:
                item = item.replace("ip route 0.0.0.0 0.0.0.0 ", '')
                parent_ip = re.findall(ipPat, item )
                parent_ip = str(parent_ip[0]).strip()
                filehand.write("\n\n  Parent IP : " + parent_ip +"\n")
                parent_device_found = "Yes"
                break
        
        if parent_device_found == "No":
            Flag = "F"
            result,Cap_Cnt,Flag = self.capCiscoRS.CaptureOutput(session,"show run | in ip default-gateway ",0,Flag,pmpt)
            result = result.split("\n")
            
            for item in result:
                if "ip default-gateway " in item:
                    item= item.strip()
                    parent_ip = item.replace("ip default-gateway ",'').strip()
                    parent_device_found = "Yes"
                    filehand.write("\n\n  Parent IP : " + parent_ip +"\n")
                    break
        
        