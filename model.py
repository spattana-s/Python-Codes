'''
Created on Apr 29, 2017

@author: sp977u

'''

class DeviceModel :
    
    def getModelInfo(self,logpath,ipadd):
        loc =0
        Final = "NF"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                
                
                if "Model number                    : WS-C2960S-24PS-L" in line or "WS-C2960S-24PS-L" in line:
                    Final = "WS-C2960S-24PS-L"
                    break
                elif "Model number                    : WS-C2960S-48FPS-L" in line or "WS-C2960S-48FPS-L" in line :
                    Final = "WS-C2960S-48FPS-L"
                    break
                elif "WS-C3560V2-24PS-S" in line or "Model number                    : WS-C3560V2-24PS-S" in line:
                    Final = "WS-C3560V2-24PS-S"
                    break
                elif "WS-C3560-48TS" in line :
                    Final = "WS-C3560-48TS"
                    break
                elif "Cisco WS-C3550-48" in line:
                    Final = "Cisco WS-C3550-48"
                    break
                elif "Cisco C6832-X-LE" in line:
                    Final = "Cisco C6832-X-LE"
                    break
                         
                elif "Model number                    : WS-C3750X-48T-L" in line or "WS-C3750X-48T-L" in line :
                    Final = "WS-C3750X-48T-L"
                    break
                elif  "Model Number     " in line and " :" in line:
                    Final = line.replace("Model Number",'')
                    Final = Final.replace(":",'')
                    Final = Final.strip()
                    break
                elif "Model number " in line and " :" in line:
                    Final = line.replace("Model number",'')
                    Final = Final.replace(":",'')
                    Final = Final.strip()
                    break
                elif "WS-C6504-E" in line:
                    Final = "WS-C6504-E"
                    break
                elif "PID: WS-C4506-E" in line or "WS-C4506-E" in line:
                    Final = "WS-C4506-E"
                    break
                elif "WS-X45-SUP8-E" in line:
                    Final = "WS-C4506-E - SUP8-E"
                    break
                elif "cisco WS-C4506" in line:
                    Final = "cisco WS-C4506"
                    break
                elif "cisco WS-C6509" in line:
                    Final = "cisco WS-C6509"
                    break
                elif "WS-C3550-12G" in line:
                    Final = "WS-C3550-12G"
                    break
                
                elif "CISCO2901/K9"  in line:
                    Final = "CISCO2901/K9"
                    break
                elif "Cisco 3845" in line:
                    Final = "Cisco 3845"
                    break
                elif "Cisco 3825" in line:
                    Final = "Cisco 3825"
                    break    
                elif "Cisco 2811" in line:
                    Final = "Cisco 2811"
                    break
                
                
                elif "Model number                    : ME-3600X-24FS-M" in line  or "ME-3600X-24FS-M" in line :
                    Final = "ME-3600X-24FS-M"
                    break


                elif "Model number                    : WS-C3750X-12S-S" in line or "WS-C3750X-12S-S" in line:
                    Final = "WS-C3750X-12S-S"
                    break
                
                elif "cisco ME-C6524GS-8S" in line or "ME-C6524GS-8S" in line :
                    Final = "cisco ME-C6524GS-8S"
                    break
                elif "CISCO3925-CHASSIS" in line:
                    Final = "CISCO 3925"
                    break
                elif "Nexus 5596 Chassis" in line :
                    Final = "Nexus 5596 Chassis"
                    break
                elif "cisco Nexus7000 C7009" in line:
                    Final = "cisco Nexus7000 C7009"
                    break
                elif "cisco Nexus 5596" in line:
                    Final = "cisco Nexus 5596"
                    break
                elif "Cisco VG224" in line or "VG224" in line :
                    Final = "Cisco VG224"
                    break
                elif "Hardware:   ASA5550" in line or "ASA 5550 Adaptive Security Appliance" in line:
                    Final ="ASA5550"
                    break
                elif  "ASA 5585-X" in line or "Hardware:   ASA5585-SSP-20" in line:
                    Final = "ASA 5585-X"
                    break
                elif "ASA 5525-X" in line or "ASA 5525-x" in line :
                    Final = "ASA 5525-X"
                    break
                elif "ASA 5510 Adaptive Security Appliance" in line or "Hardware:   ASA5510" in line:
                    Final = "ASA 5510"
                    break
                elif "ASA5520" in line :
                    Final = "ASA5520" 
                    break
                elif "ASA5555" in line:
                    Final = "ASA5555"
                    break
                #===============================================================
            
                elif "Model: ex" in line:
                    line = line.replace("Model:"," ")
                    Final = line.strip()
                    break
                
            
                elif "Model: qfx51" in line or "Model: qfx" in line:
                    line = line.replace("Model:"," ")
                    Final = line.strip()
                    break
                elif "Model:" in line:
                    line = line.replace("Model:"," ")
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
   