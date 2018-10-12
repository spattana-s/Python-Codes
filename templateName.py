'''
Created on Sep 25, 2017

@author: sp977u

'''

class templateNameDetails :
    
    def getTemplateName(self,logpath,ipadd):
        
        loc =0
        Final = "NF"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if "banner" in line and ( ".txt" in line or ".TXT" in line):
                    
                    loc2 = line.lower().rfind(".txt")
                    
                    temp = line[ : loc2 + 4]
                    
                    loc1 = temp.rfind('/')
                    
                    temp =  temp[loc1 + 1 : ]
                                   
                    Final = temp.strip()
                    break
                 
                if ("system login announcement" in line  or "announcement" in line  ) and (".txt" in line or ".TXT" in line):
                    
                    loc2 = line.lower().rfind(".txt")
                    
                    temp = line[ : loc2 + 4]
                    
                    loc1 = temp.rfind('/')  
                    
                    temp =  temp[loc1 + 1 : ]
                    
                    Final = temp.strip()
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
   