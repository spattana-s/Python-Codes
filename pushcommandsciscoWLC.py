import os
import copy
import netmiko
import time
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
from service_network.device_wheels import captures

class grindCommands:
    
    def WLC_process(self,session,ipadd,Cisco_Wifi_commands,Final_log_path,SingleOutputFile,matchLock,Devtype):
        
        pmpt = "NF"
        status= False
        Cap_Cnt =0
        capWLC = captures.outPutcaptures()   
        try :
                
            pmpt = session.find_prompt()
                
        except AttributeError as ex:
            print(ex)
            #print( "Problem in getting prompt  : ",ipadd)
            return status
        except( IOError , NetMikoTimeoutException) as ex:
            time.sleep(1.7)
            pmpt = session.find_prompt()
        except ValueError as ex:       
            print(ex)               
            #print( "Problem in getting prompt  : ",ipadd)
            return status
        except Exception as ex:
            print(ex)
            #print( "Problem in getting prompt with generic exc : ",ipadd)
            return status        
            
        if '>' not in pmpt:
            print ("Problem in getting prompt ",ipadd)
            return False
            
        ipfile = Final_log_path + "\\" +  str(ipadd) + ".txt"
                
        myfile=  open(ipfile,"w")
        hostnm = copy.copy(pmpt)
        hostnm = hostnm[:-1]
        pmpt_sh = pmpt
        myfile.write("IP address : " + ipadd )
        myfile.write("\n")
        myfile.write("Hostname : " + hostnm)
                        
        myfile.write(pmpt)
        myfile.write("\n")
        myfile.write(pmpt)
        
        pmpt = session.find_prompt()
        for cmd in Cisco_Wifi_commands:
                            
            cmd = str(cmd).strip("[").strip("]").strip("'").strip()    
            Flag = 'F'    
            time.sleep(0.3)    
            #result,Cap_Cnt,Flag = capWLC.CaptureOutput_WLC(session,"\n",0,Flag,pmpt)
                
            if cmd.startswith("show") or cmd.startswith("sho") or cmd.startswith("sh "):
                '''if session.check_config_mode() :
                     myfile.write("\n")
                     myfile.write(pmpt)
                    myfile.write("exit")
                    session.exit_config_mode()
                    pmpt = pmpt_sh '''
                        
                myfile.write("\n")
                    
                result,Cap_Cnt,Flag = capWLC.CaptureOutput_WLC(session,cmd,0,Flag,pmpt)
                                                     
            else:
                myfile.write("\n")
                myfile.write(pmpt )
                myfile.write(cmd)
                myfile.write("\n")
                    
                result,Cap_Cnt,Flag,pmpt = capWLC.RunOtherCommands(session,cmd,0,Flag,myfile)
                tem = session.send_command("\n")
                pmpt = session.find_prompt()
                myfile.write(pmpt )
                myfile.write("\n")
                    
            if Flag == 'S' :
                if len(result )>= 1 and "syntax error" not in result and "Invalid" not in result :
                    myfile.write("\n")
                    #pmpt = session.find_prompt()
                    myfile.write(pmpt)
                    myfile.write(cmd)
                    myfile.write("\n")
                    myfile.write(result)
                    
                    
                    
                    while 1:
                        
                        result,Cap_Cnt,Flag = capWLC.CaptureOutput_WLC(session,"\n",0,Flag,pmpt)
                        if len(result) == 0:
                            break
                        else:
                            myfile.write("\n")
                            myfile.write(result)
                   
                    myfile.write("\n")
                    
                       
                elif Cap_Cnt > 4 or Flag =="F":
                        
                    session.disconnect()
                    myfile.close
                    try :
                        os.remove(ipfile)
                    except PermissionError :
                        time.sleep(2)
                        myfile.close()
                        os.remove(ipfile)
                    finally:    
                        os.remove(ipfile)
                        return False
                
                    
                    
            myfile.write('\n')
            myfile.write(pmpt)
            myfile.write('\n')
            
                                                        
            
            myfile.write(pmpt)
            myfile.write("\n")
            myfile.close()
            session.disconnect()
            status = True 
            
            if status == True and SingleOutputFile == "True":
                
                flatstat = self.writeFlatfile(ipfile,ipadd,pmpt,Final_log_path)
                
        return status