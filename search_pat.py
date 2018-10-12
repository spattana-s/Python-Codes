'''
Created on Apr 16, 2018

This class is for handling VLAN and subnets info under Network tab in Speed
@author: sp977u
'''
class command_pat_search :
    
    def __init__(self):
        
        self.sucfilecontent = []
        self.hostname_written = "No"
        self.searchPat = []
        
    def write_pattern_info(self,logpath, ipadd, row,column, mySheet,style,hostnamecol,hsname,searchpat,filecontent,orange_style,green_style_txt,white_style_interface_txt ,real_col_num):
        
        self.Final = "NF"
        self.rowswritten = 0
        self.hostnamecol = hostnamecol
        self.row = row
        self.column =  column
        self.real_column_num = real_col_num
        self.ip_address = ipadd
        self.hostname = hsname
        self.mySheet = mySheet
        self.style = style
        self.orange_style_txt = orange_style
        self.green_style_txt = green_style_txt
        self.search_pat = searchpat.split(",")
        self.sucfilecontent = filecontent
        self.white_style_interface_txt = white_style_interface_txt
        
        try :
            
            if self.hostname_written == "No" :
                self.mySheet.write(self.hostnamecol + str(self.row) , hsname, style)
                self.hostname_written = "Yes"
            
            for item in self.search_pat:
                
                self.process_search_info(item)
                    
            if self.rowswritten == 0:
                self.rowswritten = 1
            return  self.rowswritten
            
        except Exception as ex:
            print("There is something wrong in write pat method under command pat search class")
            print(ex)
            if self.rowswritten == 0:
                self.rowswritten = 1
                
            return self.rowswritten
    #=======================================================================================================
    
    def process_search_info(self,pattern):
        self.current_pat = pattern
        match = "NF"
        self.parent = "NF"
        self.last_interface ="NF"
        self.current_interface = "NF"
        self.policy_found = False
        self.policy_names = []
        self.commands_set = []
        self.interface_status = "UP"
        my_prev_index = 0
        local_column_ind =0
        

        try :
        
            for ind in range(len(self.sucfilecontent)):
                
                if self.sucfilecontent[ind].lower().startswith("interface vlan"):
                    continue
        
                if self.sucfilecontent[ind].lower().startswith("interface "):
                    
                    # below to write ip add and host name for each row
                    self.mySheet.write( chr( (self.real_column_num -2) + 65 )  + str(self.row ),  self.ip_address, self.white_style_interface_txt)
                    self.mySheet.write( (chr( (self.real_column_num -1) + 65 ) + str(self.row )),  self.hostname, self.white_style_interface_txt)
                    
                    self.mySheet.write(self.column + str(self.row ),  self.sucfilecontent[ind], self.white_style_interface_txt)
                    #self.row = self.row + 1
                    #self.rowswritten = self.rowswritten + 1
                    my_prev_index = ind + 1
                    
                    for cmd  in self.sucfilecontent[my_prev_index:len(self.sucfilecontent)-1]:
                
                        if cmd.startswith("interface "): 
                            break
                    
                        else:
                            self.commands_set.append(cmd)
                        
                    for item in self.commands_set :
                        if "shutdown" == item.strip():
                            self.interface_status = "shutdown"
                        
                        if pattern in item :
                            # applying green color for policy found
                            self.mySheet.write( chr( (self.real_column_num + 1 )  + 65 ) + str(self.row ), item, self.green_style_txt)
                            self.row = self.row + 1
                            self.rowswritten = self.rowswritten + 1
                            
                            self.policy_found = True
                    if self.policy_found == False :
                        
                        if self.interface_status == "shutdown":
                            
                            self.mySheet.write(  (chr( (self.real_column_num + 1 )  + 65 ) + str(self.row )), "Missing Policy, but Interface is in Shutdown mode !", self.orange_style_txt)
                            self.row = self.row + 1
                            self.rowswritten = self.rowswritten + 1
                    
                        else:
                            self.mySheet.write(   chr( (self.real_column_num + 1) +65 )  + str(self.row ), "Missing Policy", self.orange_style_txt)
                            self.row = self.row + 1
                            self.rowswritten = self.rowswritten + 1
                        
                    self.commands_set.clear()
                    self.policy_found = False
                    self.interface_status = "UP"
                    
                
            '''    #below block for cisco devices
                if line.startswith("interface "):
                    #self.current_interface = self.last_interface[:]
                    if self.current_interface != "NF":
                        
                        self.last_interface = self.current_interface
                        
                    self.current_interface = line[:] 
            
                    self.policy_found = False
                    
                    self.mySheet.write(self.column + str(self.row ),  self.last_interface, self.style)
                    #self.last_interface = "NF"
                    self.row = self.row + 1
                    self.rowswritten = self.rowswritten + 1
            
                if "service-policy " in line.lower() and self.current_interface.startswith("interface ") :
                    self.policy_found = True
                    self.policy_name = line[:]
                    
                    if self.current_interface.startswith("interface ") and self.policy_found == True :
                    
#                       self.mySheet.write(self.column + str(self.row ),  self.last_interface, self.style)
#                         #self.last_interface = "NF"
#                         self.row = self.row + 1
#                         self.rowswritten = self.rowswritten + 1
                            
                        self.mySheet.write(self.column + str(self.row ), self.policy_name, self.orange_style_txt)
                        self.row = self.row + 1
                        self.rowswritten = self.rowswritten + 1
                        self.style.set_font_color('black')
                        self.policy_name = "NF"
                        
                if self.current_interface.startswith("interface ")  and self.current_interface != "NF" and self.last_interface.lower() != self.current_interface.lower() and self.policy_found == False :
                    self.mySheet.write(self.column + str(self.row ),  self.current_interface, self.style)
                    self.row = self.row + 1
                    self.rowswritten = self.rowswritten + 1
                    
                    self.mySheet.write(self.column + str(self.row ), "Missing Policy", self.orange_style_txt)
                    self.row = self.row + 1
                    self.rowswritten = self.rowswritten + 1
                    self.style.set_font_color('black')
                    self.policy_name = "NF"
                
                if self.current_interface.startswith("interface ") and "line vty " in line and self.policy_found == False :
                    self.mySheet.write(self.column + str(self.row ),  self.last_interface, self.style)
                    #self.last_interface = "NF"
                    self.row = self.row + 1
                    self.rowswritten = self.rowswritten + 1
                        
                        
                    self.mySheet.write(self.column + str(self.row ), "Missing Policy", self.orange_style_txt)
                    self.row = self.row + 1
                    self.rowswritten = self.rowswritten + 1
                    self.style.set_font_color('black')
                    self.policy_name = "NF"
                    
                    break
                
                    
                    
                    
                
                if  self.current_pat.lower() in line.lower() :
                    match = line[:]
                    
                    if self.parent == "NF":
                        pass
                    if self.parent.lower().strip() == self.current_pat.lower().strip() :
                        self.mySheet.write(self.column + str(self.row ),  self.parent, self.style)
                        self.parent = "NF"
                        self.row = self.row + 1
                        self.rowswritten = self.rowswritten + 1
                        
                    elif self.parent.lower().strip() != match.lower():
                        
                        self.mySheet.write(self.column + str(self.row ), self.parent, self.orange_style_txt)
                        self.row = self.row + 1
                        self.rowswritten = self.rowswritten + 1
                        self.style.set_font_color('black')
                        self.mySheet.write(self.column + str(self.row ), match, self.style)
                        self.parent = "NF"
                        
                        self.row = self.row + 1
                        self.rowswritten = self.rowswritten + 1   
                '''
                    
                
        except Exception as ex:
            print("There is something wrong in Process search info method under search_pat module !")
            print(ex)
            
    
        
                
