import os
import re
import copy
import netmiko
import time
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from service_network.device_wheels import captures
from service_network.device_wheels import devicelogin
from netaddr import IPNetwork

class grindCommands:
    
    def __init__(self):
        
        self.loginTrial = devicelogin.Login()
        self.user = ""
        self.psw = ""
        self.vlan_all = []
        
    def Juniper_process(self,session,ipadd,Juni_commands,Final_log_path,SingleOutputFile,matchLock,devtype,usr,pw):
    
        pmpt = "NF" 
        Cap_Cnt =0
        realcmd = "NF"
        self.capJuni = captures.outPutcaptures()
        self.user = usr
        self.psw = pw     
              
        try :
            pmpt = session.find_prompt()
                
        except AttributeError as ex:
            print(ex)
            #print ("Problem in getting prommpt ...!  : "+str(ipadd))
            return False 
             
        except ValueError as ex:                      
            print(ex)
            #print ("Problem in getting prommpt ...!  : "+str(ipadd))
            return False 
        except( IOError , NetMikoTimeoutException) as ex:
            time.sleep(1.7)
            pmpt = session.find_prompt()
            print(ex)
            #print ("Problem in getting prommpt ...!  : "+str(ipadd))
             
        except Exception as ex:
            print(ex)
            #print ("Problem in getting prompt juniper with generic exc : ",str(ipadd))        
            
         
        if '>' not in pmpt:
            
            return False
             
        ipfile = Final_log_path +   str(ipadd) + ".txt"
                                            
        myfile=  open(ipfile,"w")
        
        hostnm = copy.copy(pmpt)                  
        hostnm = hostnm[:-1]
        hostnm = hostnm [hostnm.find("@") + 1 : ]
        pmpt_sh = pmpt
    
        myfile.write("IP address : " + ipadd )
        myfile.write("\n")
        myfile.write("Hostname : " + hostnm)
        
        myfile.write("\n\n")
        
      
        for cmd in Juni_commands:
                    
            cmd = str(cmd).strip("[").strip("]").strip("'").strip()          
            Flag = 'F'  
            realcmd = cmd[:]
            
            if ("_ASA" in cmd or "_Cisco" in cmd or "_VG224" in cmd )  and devtype == "juniper":
                continue
            if "_Juniper" in cmd or "_General" in cmd:
                cmd = cmd [ : cmd.rfind("_") -1 ]
            
            time.sleep(0.3)  
            myfile.write("\n")   
            if cmd.startswith("show") or cmd.startswith("sho") or cmd.startswith("sh "):
                myfile.write("\n\n")
                myfile.write("{master:0}")
                myfile.write("\n")
                myfile.write(pmpt)
                myfile.write("\n")
                myfile.write("\n")
                myfile.write("{master:0}")
                myfile.write("\n")
                    
                result,Cap_Cnt,Flag = self.capJuni.CaptureOutput(session,cmd,0,Flag,pmpt)
                
                if "show configuration | match next-hop" in realcmd :
                    
                    self.get_parent_device(session, pmpt, myfile )
                
                
                if "show vlans | match vlan | no-more _Juniper" in realcmd  and Flag == "S": # block for handling vlans and subnets capturing
                    myfile.write("\n\n" + result + "\n\n")
                    self.get_vlans_info(result,myfile)
                    parent_device_found = "No"
                    # we will first try to check if there are local L3 with subnets configured
                    self.scan_subnet_details_local(session,pmpt,myfile)
                    
                    
                    
                    if len(self.vlan_all) != self.local_vlans_found :
                        Flag = "F"
                        result,Cap_Cnt,Flag = self.capJuni.CaptureOutput(session,"show configuration | match next-hop",0,Flag,pmpt)
                        parent_device_found = "No"
                        
                        myfile.write("\n" + result + "\n\n")
                        
                        result = result.split("\n")
                        
                        for item in result:
                            
                            if "0.0.0.0/0" in item and "next-hop" in item  and ";" in item:
                                
                                parent_ip  = item[ item.rfind("next-hop") : ].replace("next-hop",'').replace(";",'').strip()
                                parent_ip = str( parent_ip.strip() )
                                
                                myfile.write("\n\n  Parent IP : " + parent_ip +"\n")
                                parent_device_found = "Yes"
                                break
                        
                        if parent_device_found == "Yes" :
                            
                            parentDevtype = self.loginTrial.ScreeningDevice(parent_ip,self.user ,self.psw)
                            
                            #print("Parent ip found for : ",ipadd)
                            #print("Parent is  : ",parent_ip)
                            #print("parent dev type is : ",parentDevtype)
                            
                            self.write_vlans_from_parent(parent_ip,parentDevtype,myfile)
                            
                    result = "\n"
        
            else:
                myfile.write("\n\n")
                myfile.write("{master:0}")
                myfile.write("\n")
                myfile.write(pmpt)
                myfile.write("\n")
                myfile.write("\n")
                myfile.write("{master:0}")
                myfile.write("\n")
                myfile.write(pmpt)
                myfile.write(cmd)
                myfile.write("\n")
                result,Cap_Cnt,Flag,pmpt = self.capJuni.RunOtherCommands(session,cmd,0,Flag,myfile)
                  
            if Flag == 'S' :
                if len(result )>= 1 and "syntax error" not in result and "Invalid" not in result : 
                    myfile.write(pmpt)
                    myfile.write(cmd)
                    myfile.write("\n")
                    myfile.write(result)
            elif Flag == 'F':
                Cap_Cnt = Cap_Cnt + 1
                result,Cap_Cnt,Flag,pmpt = self.capJuni.RunOtherCommands(session,cmd,0,Flag,myfile)        
            
            if Cap_Cnt > 4 or Flag == 'F':
                        
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
                    
            myfile.write("\n\n")
            myfile.write("{master:0}")
            myfile.write("\n")
            myfile.write(pmpt)
            myfile.write("\n")
            myfile.write("\n\n")
                                  
        myfile.write("\n")
        myfile.write("\n\n")
               
        session.disconnect()
        myfile.close()
        status = True
        
        if status == True and SingleOutputFile == "True":

            flatstat = self.capJuni.writeFlatfile(ipfile,ipadd,pmpt,Final_log_path)
                
        return status
    #==========================================================================
    def get_vlans_info(self,output,filehand):
        tempvlan = "NF"
        self.output =  output.split('\n')
        self.vlan_all = []
        self.VLAN = 0
    
        for cmd in self.output:
            
            if "tag" in cmd.lower() or "interface" in cmd.lower() :
                continue
            
            if cmd.lower().strip().startswith("vlan" ) or 'vlan' in cmd.lower().strip():
                cmd = cmd.strip()
                self.VLAN = int(cmd[cmd.rfind(" ") :])
                
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
                    filehand.write("\nsingle WLC HREAP VLAN :  " + str(self.VLAN)+"\n")
                elif "4094" in str(self.VLAN):
                    filehand.write("\nNULL VLAN 4094 Status : " + str(self.VLAN)+"\n")
                else:
                    filehand.write("\nMisc / Non Standard VLAN :  " + str(self.VLAN)+"\n")   
                
            
    def scan_subnet_details_local(self,session,pmpt,filehand):
        Flag = "F"
        Cap_Cnt =0
        self.local_vlans_found = 0
        network_with_cidr = "NF"
        

        for vl in self.vlan_all:
            Flag = "F"
            
            result,Cap_Cnt,Flag = self.capJuni.CaptureOutput(session,"show interfaces terse | match ." +str(vl) ,0,Flag,pmpt)
            
            
            result = result.split('\n') 
            
            if "." in network_with_cidr and  "/" in network_with_cidr :
                network_with_cidr = ' '
            
            for item in result:
                item = item.strip()
                if str(vl) in item and "." in item and "/" in item:
                    
                    network_with_cidr  = item[item.rfind(" "):].strip()
                    
                    ip = IPNetwork(network_with_cidr)
                    network_with_cidr = str(ip.cidr)
                    
                    filehand.write( "\n" + str(vl) + " Subnet : " + network_with_cidr + '\n')
                    filehand.write("\n")
                    self.local_vlans_found += 1
                    break
                    
                        
    def write_vlans_from_parent(self,parent_ip,parent_dev_type,filehandle):
        
        GF = 4
        logstat = False
        localcmd = "NF"
        parent_pmpt = "NF"
        realsyntax = ' '
        parent_session = None
        prompt_trials =0
        try :
            
            loginstruct = self.loginTrial.decidePattern(parent_dev_type,parent_ip,self.user ,self.psw ,GF)    
            
            if loginstruct == None:
                loginstruct = self.loginTrial.decidePattern(parent_dev_type,parent_ip,self.user ,self.psw ,GF)
            
            if loginstruct != None:
                time.sleep(1)
                parent_session,logstat = self.loginTrial.trylogin(parent_ip,**loginstruct) # trail 1
        
    
            if logstat =="F":
                time.sleep(1)
                loginstruct = self.loginTrial.decidePattern(parent_dev_type,parent_ip,self.user ,self.psw ,GF)
                if loginstruct == None:
                    loginstruct = self.loginTrial.decidePattern(parent_dev_type,parent_ip,self.user ,self.psw ,GF)
                time.sleep(1)
                if loginstruct != None:
            
                    parent_session,logstat = self.loginTrial.trylogin(parent_ip,**loginstruct)  # trail  2
        
            if parent_dev_type == "cisco":
                realsyntax = "show interface vlan "
            if parent_dev_type == "juniper" :
                realsyntax = "show interfaces terse | match ."
            #show interfaces terse | match vlan.2002

        
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
                time.sleep(3)
                prompt_trials += 1
            
            '''
            if parent_session != None and parent_dev_type == "cisco":
                parent_session.enable()
                time.sleep(1)
            if parent_session != None :  
                parent_pmpt = parent_session.find_prompt()
                
            if ">"  in parent_pmpt or "#"  in parent_pmpt :
                pass
            else:
                if parent_session != None and parent_dev_type == "cisco":
                    parent_session.enable()
                time.sleep(1)
                if parent_session != None :  
                    parent_pmpt = parent_session.find_prompt()
                if ">"  in parent_pmpt or "#"  in parent_pmpt :
                    pass
                else:
                    parent_pmpt = "NF"
                
            '''
        
            if parent_pmpt != "NF" and parent_session != None :
                
                for vlan in self.vlan_all:
                    if "4094" in str(vlan):
                        continue
                    Flag = "F" # sending local vlan command to parent to get SVI info
                    localcmd = (realsyntax  + str(vlan)).strip()    
                    result,Cap_Cnt,Flag = self.capJuni.CaptureOutput(parent_session,localcmd  ,0,Flag,parent_pmpt)
                    result = result.split("\n" )
                
                    final_subnet = " "
                    for item in result :
                        if str(vlan) in item and "up" in item and "." in item and "/" in item :
                            item = item.strip()
                            final_subnet = item[ item.rfind(" ") :].strip()
                            ip = IPNetwork(final_subnet )
                            final_subnet = str(ip.cidr)
                            
                            filehandle.write("\n " + str(vlan) + " Subnet : " + final_subnet + "\n\n")
                            break
                            
                        if "Internet address is" in item and parent_dev_type == "cisco":
                            final_subnet = item.replace("Internet address is", '').strip()
                            ip = IPNetwork(final_subnet )
                            final_subnet = str(ip.cidr)
                            
                            filehandle.write("\n " + str(vlan) + " Subnet : " + final_subnet + "\n\n")
                            break
                                    
                parent_session.disconnect()
                
        except Exception as ex:
            print(" There is something wrong in get vlans from parent method in pushcommands Juniper class")
            print(ex)
            
    def get_parent_device(self,session,pmpt,filehand):
        
        Flag = "F"
           
        result,Cap_Cnt,Flag = self.capJuni.CaptureOutput(session,"show configuration | match next-hop",0,Flag,pmpt)
        parent_device_found = "No"
        result = result.split("\n")
        for item in result:
            
            if "0.0.0.0/0" in item and "next-hop" in item  and ";" in item:
                
        
                parent_ip  = item[ item.rfind("next-hop") : ].replace("next-hop",'').replace(";",'').strip()
                
                parent_ip = str( parent_ip.strip() )
                
                filehand.write("\n\n  Parent IP : " + parent_ip +"\n")
                break
            
        
            