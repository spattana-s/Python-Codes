'''
Created on May 5, 2017

@author: sp977u
'''


class prevConfchange :
    
    def configChangeDateTimeInfo(self,logpath, ipadd):
        
        Final = "NF"
        serialList = []
        rowswritten = 0
        juniScan = "N"
        
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if "Last configuration change" in line :
                    line= line.replace("! Last configuration change at", ' ')
                    loc = line.find('by')
                    Final  =  line[ :loc ]
                    Final = Final.strip()
                    break
                
                if "Configuration last modified" in line and "by" in line and "at" in line:
                    loc = line.find('at ')
                    line = line [ loc+2:]
                    Final = line.strip()
                    break
                if "Configuration has not been" in line:
                    Final = "No change since last system restart"
                    break
                if "No configuration change since" in line:
                    Final = "No change since last system restart"
                    break
                if "Last commit" in line:
                    line = line.replace("## Last commit:", ' ')
                    loc = line.find('by')
                    line = line [ : loc -1 ]
                    Final = line.strip()
                    break
                
                if not line:
                    break
                if line =="\n":
                    continue
            sucFile.close()
            #print( partNoList)
            return Final
            
        except Exception as ex:
            print(ex)
            sucFile.close()
            return "NF"
    #===
