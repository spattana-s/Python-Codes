
#import sys
#import io

from service_network.excelerator import partNoaudit
from service_network.excelerator import auditSerialDescript
from service_network.excelerator import imageInfo
from service_network.excelerator import model
from service_network.excelerator import templateVersion
from service_network.excelerator import lastConfigChange
from service_network.excelerator import ASPRfind
from service_network.excelerator import templateName
from service_network.excelerator import exceptionInfo
from service_network.excelerator import vlans_and_subnets
from service_network.excelerator import parent_device
from service_network.excelerator import search_pat



class burnfinalExcel :
    
    burnPartnum = partNoaudit.partNoNameauditTab()
    burnauditserialDescr = auditSerialDescript.auditSerial_Description()
    burnImageinfo = imageInfo.imageInformation()
    burnModel = model.DeviceModel()
    templatever = templateVersion.templateVer()
    lastConf = lastConfigChange.prevConfchange()
    toKnowASPRstatus = ASPRfind.ASPRACL()
    toKnowtemplatename = templateName.templateNameDetails()
    toknowExceptionStatus = exceptionInfo.exceptionDetails()
    togetParentDevice =  parent_device.ParentDeviceInfoNetworkTab()
    
    
    def __init__(self):
        
        self.vlans_subnets_engine = vlans_and_subnets.VlansAndSubnetsNetworkTab()
        self.search_command = search_pat.command_pat_search()
    
    def getHostinfo(self,logpath,ipadd):
        loc = 0
        Final = "NF"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if "Hostname" in line :
                    loc = line.find(':')
                                        
                    Final  = line[loc +1 :]
                    if '@' in Final:
                        loc = Final.find('@')
                        Final = Final[loc +1 :]
                        
                    break
                
                if not line:
                    break
                if line =="\n":
                    continue
            sucFile.close()
            return Final
            
        except Exception as ex:
            print(ex)
            sucFile.close()
            return "NF"
            
            
        
    def getGeneralSerialnoInfo(self,logpath,ipadd):
        
        matchfound = "F"
        Final = "NF"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if "System serial number" in line :
                    loc = line.find(':')
                    Final  = line[loc +1 :]
                    break
                if "Processor board ID" in line:
                    line = line.replace("Processor board ID", "  ")
                    Final =  line.strip()
                    break
                
                    
                if "PID: WS-C4506-E" in line and "VID:" in line and "SN:" in line:
                    loc1 = line.find('SN:')
                    line = line [loc1 : ]
                    line = line.replace('SN:', ' ')
                    Final = line.strip()
                    break
                
                if "Item" in line and "Part number" in line and "Serial number" in line and "Descri" in line:
                    loc1= line.find("Serial")
                    loc2 = line.find("Descript")
                    
                    line = sucFile.readline()
                    line = line[loc1:loc2-1]
                    Final = line.strip()
                    matchfound = "T"
                    break
                if "Chassis" in line and "DESCR" in line and "ASA" in line :
                    line = sucFile.readline()
                    loc1 = line.find('SN:')
                    line = line [loc1 : ]
                    line = line.replace('SN:', ' ')
                    Final = line.strip()
                    break
                if "PID: " in line and "VID:" in line and "SN: " in line:
                    loc1 = line.find("SN:")
                    line= line[loc1 :]
                    line= line.replace("SN:",'')
                    Final = line.strip()
                    break
                
                if not line:
                    break
                if line =="\n":
                    continue
            sucFile.close()
            return Final
            
        except Exception as ex:
            print(ex)
            sucFile.close()
            return "NF"
            
     
            
        
    def getFlashfreeInfo(self,logpath,ipadd): 
     
        matchfound = "F"
        Final = "NF"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                
                if "bytes available" in line and "bytes used)" in line:
                    loc = line.find('bytes available (')
                    line  =  line[:loc ]
                    line = line.strip()
                    line = int(line)
                    line = (line / 1024 )/1024
                    line = round(line,2)
                    Final =str(line) + " MB"
                    matchfound = "T"
                    break
                
                    
                if "bytes free)" in line :
                    loc = line.find('(')
                    line  =  line[loc +1 : ]
                    line= line.replace(')'," ")
                    line = line.replace('bytes free'," ")
                    line = line.strip()
                    line = int(line)
                    line = (line / 1024 )/1024
                    line = round(line,2)
                    Final =str(line) + " MB"
                    matchfound = "T"
                    break
                
                if "bytes available (" in line:
                    
                    loc1 = line.find('bytes available (')
                    num1 = line[ : loc1]
                    num1 = num1.strip()
                    
                    loc1 = line.find('(')
                    
                    num2 = line[loc1+1:]
                    
                    loc2 = num2.find(' ')
                    
                    num2 = num2[ : loc2]
                    num2 = num2.strip()
                    
                    num1 = int(num1)
                    num2 = int(num2)
                    mem = num1 - num2 
                    mem = round( (mem /1024)/1024 ,2)
                    
                    Final = str(mem) + " MB"                    
                    matchfound = "T"
                    break
                
                if not line:
                    break
                if line =="\n":
                    continue
            sucFile.close()
            return Final
            
        except Exception as ex:
            print(ex)
            sucFile.close()
            return "NF"
     

    
    #=========================================================================================