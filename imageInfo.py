'''
Created on Apr 29, 2017

@author: sp977u

'''

class imageInformation :
    
    def getImageInfo(self,logpath, ipadd):
        
        matchfound = "F"
        Final = "NF"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if "System image file" in line :
                    loc = line.find(':')
                    
                    Final  =  line[loc +1 : ]
                    Final = Final.replace('"'," ")
                    loc = Final.find("/")
                    Final = Final[loc +1: ]
                    Final = Final.strip()
                    
                    matchfound = "T"
                    break
                    
                if "Base OS Software Suite" in line:
                    
                    loc = line.find('[')
                    line  = line[loc +1 :]
                    Final = line.replace(']', " ").strip()
                    
                    matchfound = "T"
                    break
                
                if "JUNOS EX  Software Suite" in line:
                    loc = line.find('[')
                    line  = line[loc +1 :]
                    Final = line.replace(']', " ").strip()
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
    