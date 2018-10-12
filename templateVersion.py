'''
Created on Apr 29, 2017

@author: sp977u

'''

class templateVer :
    
    def getTemplateversion(self,logpath,ipadd):
        
        loc =0
        Final = "NF"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if "banner" in line and ( "9." in line or "10." in line or "11." in line or "12." in line or "13." in line or "14." in line or "15." in line or "16." in line or "17." in line or "18." in line or "19." in line or "20." in line):
                    loc1 = line.find("/")
                    loc2 = line.rfind("/")
                    line = line[loc1 + 1 :loc2-1]
                    if (line.rfind("/") != -1 ):
                        line= line [ : line.rfind("/")]
                    
                    Final = line.strip()
                    break
                 
                if ("system login announcement" in line  or "announcement" in line  ) and "/" in line:
                    loc1 = line.find("/")
                    loc2 = line.rfind("/")
                    line = line[loc1 + 1 :loc2-1]
                    
                    if (line.rfind("/") != -1 ):
                        line= line [ : line.rfind("/")]
                    
                                        
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
   