'''
Created on Apr 22, 2018

This class is for handling Parent device info under Network tab in Speed
@author: sp977u
'''
class ParentDeviceInfoNetworkTab :
    
    def __init__(self):
        
        self.sucfilecontent = []
        self.hostname_written = "No"
        
    def write_parent_dev_info(self,logpath, ipadd,filecontent):
        
        Final = " "
        rowswritten = 0
        
    
        self.sucfilecontent = filecontent
        
        try :
            
        
            for line in self.sucfilecontent:
                
                if  'Parent IP :' in line  :
                    
                    
                    Final  =  line.replace("Parent IP :",'').strip()
                    
                    
                    break
                    
            
            return  Final
            
        except Exception as ex:
            print("There is something wrong in write Parent device method under parent device module ")
            print(ex)
            
                
            return " "
    #=======================================================================================================
        