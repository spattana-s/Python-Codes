'''
Created on May 1, 2017

@author: sp977u
'''

import sys

class Auditcommands :
    
    def prepareAuditcustomCommands(self,extList):
        cmdList = []
        item = 0
        
        for item in range(len(extList)) :
            
            if extList[item] == "Model":
                cmdList.append("show version _General")
                
                cmdList.append("show inventory _Cisco")
                cmdList.append("show invent _ASA")
                cmdList.append("show chassis hardware _Juniper")
                cmdList.append("show versi _General")
                
            if extList[item] == "Serial Number General":
                cmdList.append("show version _General")
                cmdList.append("show inven _Cisco")
                cmdList.append("show invent _ASA")
                cmdList.append("show chassis hardware _Juniper")
                
            if extList[item] == "OS version":
                cmdList.append("show version _General")
                
            if extList[item] == "Template version" or extList[item] == "Template Name":
                cmdList.append("show run | in banner _Cisco")
                cmdList.append("show run | in banner _ASA")
                cmdList.append("show configuration system login announcement | display set _Juniper")
                cmdList.append("show configuration | match announcement")
                
                
            if extList[item] == "Flash free bytes":    
                cmdList.append("show flash: _Cisco")
                cmdList.append("show bootflash: _Cisco")
                cmdList.append("show bootdisk: _Cisco")
                cmdList.append("show bootvar: _Cisco")
                cmdList.append("show flash: _ASA")
                cmdList.append("show disk0: _ASA")
                cmdList.append("show slot0: _VG224")
                
            if extList[item] == "Last Config Date":    
                cmdList.append("show run | in configuration change _Cisco")
                cmdList.append("show version _ASA")
                cmdList.append("show configuration | match Last  _Juniper")
            if extList[item] == "ASPR ACL present:Yes/No ?": 
                cmdList.append("show access-lis al_vty_access_aspr _Cisco")
                cmdList.append("show access-list al_vty_access_aspr _Cisco")
                cmdList.append("show run | in al_vty_access_aspr _Cisco")
                cmdList.append("show run | in vty _Cisco")
                cmdList.append("show access-list _Cisco")
                
                cmdList.append("show configuration | match pl_ssh_access_aspr  _Juniper")
                cmdList.append("show configuration | match ssh_access_aspr  _Juniper")
                cmdList.append("show run ssh _ASA")
                cmdList.append("show runn | in ssh _ASA")
            
            if  extList[item] == "Exception":
                cmdList.append("show run | in banner _Cisco")
                cmdList.append("show running | in banner _Cisco")
                cmdList.append("show run | in banner _ASA")
                cmdList.append("show configuration system login announcement | display set _Juniper")
                cmdList.append("show configuration | match announcement")
            
            if extList[item] == "MGMT VLAN" or extList[item] == "Data VLAN" or extList[item] == "Voice VLAN" or extList[item] == "Wireless VLAN" or extList[item] == "Other VLAN" :
                cmdList.append("show run vlan _Cisco")
                cmdList.append("show vlans | match vlan | no-more _Juniper")
                
                
            if extList[item] == "Part Number" or   extList[item] == "Part Name" or extList[item] == "Serial Number Audit" or extList[item] == "Description":
                cmdList.append("show inventory _Cisco")
                cmdList.append("show inven  _ASA")
                cmdList.append("show chassis hardware _Juniper")
                
            if extList[item] == "Parent / Neighbor Device" :
                cmdList.append("show configuration | match next-hop _Juniper")
                cmdList.append("show run | in ip route 0.0.0.0 _Cisco")
            if extList[item] == "Search Pattern" :
                cmdList.append("show configuration | no-more _Juniper")
                cmdList.append("show run _Cisco")
                cmdList.append("show run _ASA")
            
            
        cmdList = set(cmdList)
        cmdList = list(cmdList)
        return cmdList
    
        
       
    