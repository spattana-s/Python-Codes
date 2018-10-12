'''
Created on June 15, 2017

@author: sp977u
'''


class ASPRACL :
    
    def doIhaveASPRaclInfo(self,logpath, ipadd):
        
        Final = "NF"
        serialList = []
        rowswritten = 0
        juniScan = "N"
        
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if "show" in line or "sho" in line :
                    continue
                if "pl_ssh_access_aspr" in line :
                    Final  = "Yes"
                    break
                
                
                if ("access-list" in line and "vty" in line ) or "standard al_vty_access_aspr" in line or "Standard IP access list al_vty_access_aspr" in line or "access list al_vty_access_aspr" in line or "ACL al_vty_access_aspr" in line  :
            
                    Final = "Yes"
                    break
                
                
                if "ssh 9." in line or "ssh 135." in line or "ssh 10." in line:
                    Final = "Yes"
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
            return "Fail"
    #===
