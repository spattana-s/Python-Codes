'''
Created on Apr 16, 2018

This class is for handling VLAN and subnets info under Network tab in Speed
@author: sp977u
'''
class VlansAndSubnetsNetworkTab :
    
    def __init__(self):
        
        self.sucfilecontent = []
        self.hostname_written = "No"
        
    def write_MDVO_vlan_info(self,logpath, ipadd, row,column, mySheet,style,hostnamecol,hsname,searchpat,filecontent):
        
        Final = "NF"
        rowswritten = 0
        vlanfound = "No"
        mgmtvlan = "NF"
        
        self.searchPat = searchpat
        self.sucfilecontent = filecontent
        
        try :
            
            if self.hostname_written == "No" :
                mySheet.write(hostnamecol + str(row) , hsname, style)
                self.hostname_written = "Yes"
                
            for line in self.sucfilecontent:
                
                if  self.searchPat in line  :
                    
                    loc = line.rfind(':')
                    Final  =  line[loc+1 : ]
                    mgmtvlan = Final[:].strip()
                    Final = "VLAN " + Final.strip() + " ;  "
                    vlanfound = "Yes"
                        
                    subnet = self.scan_subnet_info(mgmtvlan)
                    
                    Final = Final + subnet    
                    temprow = str(row)
                    
                    mySheet.write(column + str(temprow),  Final, style)
                    row = row + 1
                    rowswritten = rowswritten + 1
                    Final = ' '
                    vlanfound = "No"
                    
            if rowswritten == 0:
                rowswritten = 1
            return  rowswritten
            
        except Exception as ex:
            print("There is something wrong in write mgmt vlan method under vlans and subnets class")
            print(ex)
            if rowswritten == 0:
                rowswritten = 1
                
            return rowswritten
    #=======================================================================================================
    
    def write_wireless_vlan_info(self,logpath, ipadd, row,column, mySheet,style,hostnamecol,hsname,filecontent):
        
        Final = "NF"
        rowswritten = 0
        vlanfound = "No"
        wirelessvlan = "NF"
        
        self.sucfilecontent = filecontent
        
        try :
        
            if self.hostname_written == "No" :
                mySheet.write(hostnamecol + str(row) , hsname, style)
                self.hostname_written = "Yes"
                
            for line in self.sucfilecontent:
                
            
                if  "BLUE WIRELESS VLAN" in line or "GUEST WIRELESS VLAN" in line or "YELLOW WIRELESS VLAN" in line or "single WLC global MGMT VLAN" in line or "single WLC Transport VLAN" in line or "single WLC VE Transport VLAN" in line or "single WLC HREAP VLAN" in line  :
                
                    loc = line.rfind(':')
                    Final  =  line[loc+1 : ]
                    wirelessvlan = Final[:].strip()
                    Final = "VLAN " + Final.strip() + " ;  "
                    vlanfound = "Yes"
                        
                    subnet = self.scan_subnet_info(wirelessvlan)
                    
                    Final = Final + subnet    
                    temprow = str(row)
                    
                    mySheet.write(column + str(temprow),  Final, style)
                    row = row + 1
                    rowswritten = rowswritten + 1
                    Final = ' '
                    vlanfound = "No"
                    
            
            if rowswritten == 0:
                rowswritten = 1
                
            return  rowswritten
            
        except Exception as ex:
            print("There is something wrong in write mgmt vlan method under vlans and subnets class")
            print(ex)
            if rowswritten == 0:
                rowswritten = 1
                
            return rowswritten

    
    def scan_subnet_info(self,vlan):
        subnet = ""
        
        for item in self.sucfilecontent:
            
            if vlan in item and "Subnet" in item and ":" in item :
                subnet =  item[ item.rfind(":") +1 : ]    
                break
                
        return subnet
        