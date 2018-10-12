
import netmiko
import time

from netmiko import NetMikoTimeoutException, NetMikoAuthenticationException
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import threading

class outPutcaptures :
    
    matchLock = threading.Lock()    
    
    def CaptureOutput(self,session,cmd,Cap_Cnt,Flag,prmpt):
        
        data = "NF"
        showFlag= "N"
        
        if "show running-config" in cmd or 'show run' in cmd or "show inve" in cmd or  "show configuration | no-more" in cmd or "show configuration | no-more | display set" in cmd or "show interface terse" in cmd or "show run-config commands" in cmd:
            DF = 4
        else:
            DF = Cap_Cnt + 3
            
        try :
              
            #res = session.send_command(cmd,strip_prompt=False)
            #res = session.send_command_timing(cmd,delay_factor=2,max_loops=150,strip_prompt=False,strip_command=True, normalize=True )
            
            #res = session.send_command_expect(cmd,delay_factor=DF,strip_prompt=False, normalize=True )
            
            res = session.send_command_expect(cmd,strip_prompt=False)
            
            time.sleep(0.1)
            
        
            if "error: error communicating with fpc" in res  or "error: error communicating" in res:
                time.sleep(5)
                #res = session.send_command(cmd,strip_prompt=False)
                #res = session.send_command_timing(cmd,delay_factor=2,max_loops=150,strip_prompt=False,strip_command=True, normalize=True )
                
                #res = session.send_command_expect(cmd,delay_factor=DF,strip_prompt=False, normalize=True )
                
                res = session.send_command_expect(cmd,strip_prompt=False)
                
                time.sleep(0.1)
            
            if "error: error communicating with fpc" in res  or "error: error communicating" in res:
                time.sleep(0.5)
                Flag = 'F'  
                return res,Cap_Cnt,Flag
            
        
            if prmpt in res:
                Flag = 'S'
            else:
                Flag = 'F'
                res = "Bad result"
            return res,Cap_Cnt,Flag
                       
        except IOError :
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(1.5)
                result_tmp,Cap_Cnt_tmp,Flag_tmp= self.CaptureOutput(session,cmd,Cap_Cnt,Flag,prmpt)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp
            else:
                Cap_Cnt = Cap_Cnt +1
                return "Bad result",Cap_Cnt,"F"
            
        except NetMikoTimeoutException :
           
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(2)
                result_tmp,Cap_Cnt_tmp,Flag_tmp= self.CaptureOutput(session,cmd,Cap_Cnt,Flag,prmpt)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp
            else:
                Cap_Cnt = Cap_Cnt +1
                return "Bad result",Cap_Cnt,"F"
            
        except Exception:
        
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(1.5)
                result_tmp,Cap_Cnt_tmp,Flag_tmp = self.CaptureOutput(session,cmd,Cap_Cnt,Flag,prmpt)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp
            else :
                Flag= 'F'
                Cap_Cnt = Cap_Cnt +1
                result_tmp = "Bad result" 
                return result_tmp,Cap_Cnt,Flag
        
        #return res, Cap_Cnt, Flag
    # ********************    below is for other than show
    def CaptureOutput_WLC(self,session,cmd,Cap_Cnt,Flag,prmpt):
        
        #res = " "
        data = "NF"
        showFlag= "N"
                        
        DF= 1
        
        if cmd == "\n":
            DF = 0.3
            
        try :
              
            #session.clear_buffer()
                                
            #res = session.send_command_expect(cmd,delay_factor= DF)
            res = session.send_command(cmd)
            time.sleep(0.2)
            if prmpt in res:
                Flag = 'S'
            else:
                Flag = 'F'
            
            return res,Cap_Cnt,Flag
                       
        except IOError :
            #session.clear_buffer()
            
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(1.5)
                result_tmp,Cap_Cnt_tmp,Flag_tmp= self.CaptureOutput_WLC(session,cmd,Cap_Cnt,Flag,prmpt)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp
            else:
                return " ",Cap_Cnt,Flag
                
        except NetMikoTimeoutException :
           # session.clear_buffer()
            
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(1.5)
                result_tmp,Cap_Cnt_tmp,Flag_tmp= self.CaptureOutput_WLC(session,cmd,Cap_Cnt,Flag,prmpt)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp
            else:
                return " ",Cap_Cnt,Flag
        except Exception:
           # session.clear_buffer()
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(1)
                result_tmp,Cap_Cnt_tmp,Flag_tmp = self.CaptureOutput_WLC(session,cmd,Cap_Cnt,Flag,prmpt)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp
            else :
                Flag= 'F'
                Cap_Cnt = Cap_Cnt +1
                result_tmp = "Error" 
                return result_tmp,Cap_Cnt_tmp,Flag
            
    def RunOtherCommands(self,session,cmd,Cap_Cnt,Flag,FileHand):
        
        data = "NF"
        showFlag= "N"
        DF= 3
        res = " "
            
        try :
              
            prompt = session.find_prompt()
                
            if cmd.startswith("wr") or cmd.startswith("wri") :
                if session.check_config_mode() :
                    session.exit_config_mode()
                res = session.send_command(cmd,delay_factor= DF)
                #res = session.send_command("\n")
                Flag = 'S'
                return res, Cap_Cnt, Flag,prompt
                
            if cmd.startswith("set") or cmd.startswith("delete") :
                res = session.send_command(cmd,delay_factor= DF)
                #FileHand.write("\n")
                #FileHand.write(res)
                #res = session.send_command("\n")
            elif cmd.startswith("commit"):
                
                res = session.send_command(cmd,delay_factor= DF)
                FileHand.write(res)
            elif cmd.startswith("reload") or cmd.startswith("reboot"):
                if session.check_config_mode() :
                    session.exit_config_mode()
                res = session.send_command(cmd,delay_factor= DF)
                FileHand.write("\n")
                FileHand.write(res)
                time.sleep(0.5)
                
                res = session.send_command("\n\r")
                res = session.send_command("\n\r")
                
            elif cmd.startswith("copy"):
                if session.check_config_mode() :
                    session.exit_config_mode()
                res = session.send_command(cmd,delay_factor= DF)
                #time.sleep(0.2)
                #FileHand.write("\n")
                #FileHand.write(res)
                #res = session.send_command("\n")
                #res = session.send_command("\n\n")
            
            elif cmd.startswith("conf"):
                    CNF ="T"
                    
                    res = session.config_mode()
                    Flag = 'S'
                    res = " "
                    prompt = session.find_prompt()
                    return res,Cap_Cnt, Flag,prompt
            elif cmd.startswith("exit") or cmd.startswith("exi") :
                    session.exit_config_mode()
                    res = " "
                    Flag = 'S'
                    tem= session.send_command("\n")
                    prompt = session.find_prompt()
                    #return res,Cap_Cnt,Flag,prompt
                    #res = session.send_command(cmd)
            
            else:
                
                res = session.send_command(cmd)
                #print(res)
                
                if "Halt the system ?" in res:
                    FileHand.write("\n")
                    FileHand.write(res)
                    res= "  "
                    #print("I have reached halt section")
                    res = session.send_command("yes")
                    res = session.send_command("\n")
                    FileHand.write("\n")
                    FileHand.write(res)
                    time.sleep(0.3)
                    
                #res = session.send_command(cmd,delay_factor= DF)
                Flag = 'S'
                if res == None or res =='':
                    res = "  "
                
                prompt = session.find_prompt()
                #return res,Cap_Cnt,Flag,prompt
            if "?" in res or "confirm" in res:
                FileHand.write("\n")
                FileHand.write(res)
                res= "  "
                res = session.send_command("\n")
                
                #if "?" not in res or "confirm" not in res:
                #  res = session.send_command("\n")
            if "?" in res or "confirm" in res:
                FileHand.write("\n")
                FileHand.write(res)
                res = "  "
                res = session.send_command("\n")
                
                if "?" not in res or "confirm" not in res:
                    res = session.send_command("\n")
                    
            #data = res.encode('utf-8')
            
            if res == None or res =='':
                res = " "
            Flag = 'S'
            return res,Cap_Cnt,Flag,prompt
    
        except IOError :
            #session.clear_buffer()
            
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(1.5)
                result_tmp,Cap_Cnt_tmp,Flag_tmp,pmtmp= self.RunOtherCommands(session, cmd, Cap_Cnt, Flag, FileHand)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp,pmtmp
            else:
                return " ",Cap_Cnt,Flag," "
            
        except NetMikoTimeoutException :
            #session.clear_buffer()
            
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(2)
                result_tmp,Cap_Cnt_tmp,Flag_tmp,pmtmp= self.RunOtherCommands(session, cmd, Cap_Cnt, Flag, FileHand)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp,pmtmp
            else:
                return " ",Cap_Cnt,Flag," "
            
        except ValueError:
            #session.clear_buffer()
            
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(1)
                result_tmp,Cap_Cnt_tmp,Flag_tmp,pmtmp= self.RunOtherCommands(session, cmd, Cap_Cnt, Flag, FileHand)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp,pmtmp
            else:
                return " ",Cap_Cnt,Flag," "
        except Exception:
           
            Flag= 'F'
            Cap_Cnt = Cap_Cnt +1
            if Cap_Cnt <= 4:
                time.sleep(1)
                result_tmp,Cap_Cnt_tmp,Flag_tmp,pmtmp= self.RunOtherCommands(session, cmd, Cap_Cnt, Flag, FileHand)
                return result_tmp,Cap_Cnt_tmp,Flag_tmp,pmtmp
            else :
                Flag= 'F'
                Cap_Cnt = Cap_Cnt +1
                result_tmp = "Error" 
                pmtmp= " "
                return result_tmp,Cap_Cnt_tmp,Flag,pmtmp
        
    def writeFlatfile(self,logpath,ipadd,hostname,Final_log_path):
        
        self.matchLock.acquire()
        try :
          
          
            pathhandle = open(logpath,"r")
        
            flathandle = open(Final_log_path + "\\Matches_Found_All.txt","a+")
            
            hostname = hostname.rstrip('#')
            hostname = hostname.rstrip('>')
            
            flathandle.write("\n\n")
            flathandle.write("===============================================================================\n\n")
            
            flathandle.write("\n\n")
            
        except Exception as uex:
            
            print("There is issue with File operation...", ipadd)
            
            print(uex )
            
            return False
                          
        while(1):
            
            line = pathhandle.readline()
                
            
            if not line:break
            
            
            flathandle.write(line)
            time.sleep(0.1)
            
            if not line : continue
             
            
            
        flathandle.write("\n")
                       
        flathandle.close()
        pathhandle.close()
        
        self.matchLock.release()
        
        return True