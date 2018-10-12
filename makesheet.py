'''
This class has d

'''

import xlsxwriter

from service_network.excelerator import burnFinalexceldata


class makeExcel:
    
    def __init__(self,):
        
        self.search_command = "NF"
     
    def prepareSheet(self,logpath,totFields,extlist):
        
        self.extList = extlist
        sucFile = None
        self.totalFields  = totFields
        self.rowsWritten =0
        localrow = 0
        self.subrows = 0
        self.writtenFlag = 'N'
        self.max_rows_written = 0
        self.burnSheet = burnFinalexceldata.burnfinalExcel()
        self.row =1
        self.FieldsDict = { }
        
        try :
            
            self.mybook = xlsxwriter.Workbook(logpath + "\\Data Sheet.xlsx")
            self.mySheet = self.mybook.add_worksheet()
            self.style = self.mybook.add_format({'bold': True})
            self.style.set_font_size(11)
            self.style.set_bg_color('yellow')
            self.style.set_font_color('black')
            
            
            self.white_style_interface_txt = self.mybook.add_format({'bold':True, 'font_color': 'black'})
            
            self.orange_style_txt = self.mybook.add_format({'bold':False, 'font_color': 'red'})
            
            self.green_style_txt = self.mybook.add_format({'bold':False,'font_color' : 'green' })
            
            
            col =0
            for col in range(len(self.extList)):
                if self.extList[col] == "Serial Number General" or self.extList[col] == "Serial Number Audit" :
                    self.mySheet.write(chr(col+65) + str(self.row), "Serial Number", self.style)
                
                else:
                    self.mySheet.write(chr(col+65) + str(self.row), self.extList[col], self.style)
                
        
            self.mySheet.set_column('A:' + chr(col + 65), 25)
            
            self.style = self.mybook.add_format({'bold': False})
            self.style.set_font_size(11)
            
            #mybook.close()
            
        except Exception as ex :
            print(ex)
            return False
        
        try :
            sucFile = open(logpath + "\\Final_log.txt" , 'r')
            
            finallog_content = sucFile.readlines()
            
            sucFile.close()
            
            for line in finallog_content:
                
                if ": Success" in line :
                    ipadd = line[ : line.rfind(':')]
                    ipadd = ipadd.strip()
                    self.row = self.row + 1
                    self.prepareData(ipadd,logpath)
                     
            
        except Exception as ex:
            print(ex)
            return False
        
        self.mybook.close()
            
        return True
    def prepareData(self,ipadd,logpath):
        self.finalAttrib = []
        item =0
        matchStr ="NF"
        self.max_rows_written = 0
        self.Auditvartouched = "N"
        self.network_attrib_touched = "No"
        self.search_attrib_touched = "No"
        partNolist = []
        hostname = matchStr = self.burnSheet.getHostinfo(logpath,ipadd)
        
        for col in range(len(self.extList)):
            
            if self.extList[col] =="Hostname":
                hostnamecol = chr(col + 65)
                break
        # reading log file , passing list to far method
        try :
            
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            self.sucfilecontent = sucFile.readlines()
            
            sucFile.close()
        except Exception as ex:
            print("There is something wrong in make sheet method , log file opening section")
            print(ex)
            sucFile.close()
            return False
        
        
        for item in range(len(self.extList)):
            
            matchStr = "NF"
            
            if self.extList[item] == "IP Address":
                self.finalAttrib.append(ipadd)
                self.writeSheet("IP Address")
            if self.extList[item] =="Hostname":
                matchStr = self.burnSheet.getHostinfo(logpath,ipadd)
                self.finalAttrib.append(matchStr)
                self.writeSheet("Hostname")
            if  self.extList[item] == "Model":
                matchStr = self.burnSheet.burnModel.getModelInfo(logpath, ipadd)
                self.finalAttrib.append(matchStr)
                self.writeSheet("Model")
            
            if self.extList[item] == "Parent / Neighbor Device" : 
                matchStr= self.burnSheet.togetParentDevice.write_parent_dev_info(logpath, ipadd,self.sucfilecontent)
                self.finalAttrib.append(matchStr)
                self.writeSheet("Parent / Neighbor Device")
            
            
            if self.extList[item] == "Serial Number General":
                matchStr = self.burnSheet.getGeneralSerialnoInfo(logpath, ipadd)
                self.finalAttrib.append(matchStr)
                if self.Auditvartouched == "Y":
                    self.row = self.row - self.rowsWritten
                self.writeSheet("Serial Number General")
                if self.Auditvartouched == "Y":
                    self.row = self.row - self.rowsWritten
            
            if self.extList[item] == "OS version":
                matchStr = self.burnSheet.burnImageinfo.getImageInfo(logpath, ipadd)
                self.finalAttrib.append(matchStr)
                if self.Auditvartouched == "Y":
                    self.row = self.row - self.rowsWritten
                self.writeSheet("OS version")
                if self.Auditvartouched == "Y":
                    self.row = self.row - self.rowsWritten
            
            if self.extList[item] == "Template version":
                matchStr = self.burnSheet.templatever.getTemplateversion(logpath, ipadd)
                self.finalAttrib.append(matchStr)
                if self.Auditvartouched == "Y":
                    self.row = self.row - self.rowsWritten
                self.writeSheet("Template version")
                if self.Auditvartouched == "Y":
                    self.row = self.row - self.rowsWritten
            if self.extList[item] == "Template Name":
                matchStr = self.burnSheet.toKnowtemplatename.getTemplateName(logpath, ipadd)
                self.finalAttrib.append(matchStr)
                if self.Auditvartouched == "Y":
                    self.row = self.row - self.rowsWritten
                self.writeSheet("Template Name")
                if self.Auditvartouched == "Y":
                    self.row = self.row - self.rowsWritten
            
            if self.extList[item] == "Flash free bytes":
                matchStr = self.burnSheet.getFlashfreeInfo(logpath, ipadd)
                self.finalAttrib.append(matchStr)
                self.writeSheet("Flash free bytes")
            
            if self.extList[item] == "Last Config Date":
                matchStr = self.burnSheet.lastConf.configChangeDateTimeInfo(logpath, ipadd)
                self.finalAttrib.append(matchStr)
                self.writeSheet("Last Config Date")
            
            if self.extList[item] == "ASPR ACL present:Yes/No ?":
                matchStr = self.burnSheet.toKnowASPRstatus.doIhaveASPRaclInfo(logpath, ipadd)
                self.finalAttrib.append(matchStr)
                self.writeSheet("ASPR ACL present:Yes/No ?")
            
            if self.extList[item] == "Exception":
                exceptionDetails = " "
                matchStr,exceptionDetails= self.burnSheet.toknowExceptionStatus.doIhaveExceptioinInfo(logpath, ipadd)
                self.finalAttrib.append(matchStr)
                self.writeSheet("Exception")
            if self.extList[item] == "Exception Details":
                self.finalAttrib.append(exceptionDetails)
                self.writeSheet("Exception Details")
            
            
            if self.extList[item] == "Part Number":
                col = 0
                for col  in range(len(self.extList)) :
                   
                    if self.extList[col] == "Part Number":
                        colValue = chr(col  + 65)
                        break
                
                partNolist, self.rowsWritten  = self.burnSheet.burnPartnum.getPartnoInfo(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname)
                
                self.rowsWritten = self.rowsWritten - 1
                self.row = self.row  + self.rowsWritten
                self.Auditvartouched = "Y"
                
            if self.extList[item] == "Part Name":
                col = 0
                if self.Auditvartouched == "Y":
                    self.row = self.row  - self.rowsWritten
                for col  in range(len(self.extList)) :
                    if self.extList[col] == "Part Name":
                        colValue = chr(col  + 65)
                        break
                
                partNamelist, self.rowsWritten  = self.burnSheet.burnPartnum.getPartnameInfo(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname)
                
                self.rowsWritten = self.rowsWritten - 1
                self.row = self.row  + self.rowsWritten
                self.Auditvartouched = "Y"
            
            if self.extList[item] == "Serial Number Audit":
                col = 0
                if self.Auditvartouched == "Y":
                    self.row = self.row  - self.rowsWritten
               
                for col  in range(len(self.extList)) :
                   
                    if self.extList[col] == "Serial Number Audit":
                        colValue = chr(col  + 65)
                        break
                
                partNolist, self.rowsWritten  = self.burnSheet.burnauditserialDescr.getauditSerialnoInfo(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname)
                self.rowsWritten = self.rowsWritten - 1
                self.row = self.row  + self.rowsWritten
                self.Auditvartouched = "Y"
                
            if self.extList[item] == "Description":
                col = 0
                if self.Auditvartouched == "Y":
                    self.row = self.row  - self.rowsWritten
               
                for col  in range(len(self.extList)) :
                   
                    if self.extList[col] == "Description":
                        colValue = chr(col  + 65)
                        break
                
                descrList, self.rowsWritten  = self.burnSheet.burnauditserialDescr.getDescriptionInfo(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname)
                self.rowsWritten = self.rowsWritten - 1
                self.row = self.row  + self.rowsWritten
                self.Auditvartouched = "Y"
            # below section for network subnets handling under network tab:
            if self.extList[item] == "MGMT VLAN"  :
                col = 0
                
                #if self.network_attrib_touched == "Yes" :
                #    self.row = self.row  - self.rowsWritten
                for col  in range(len(self.extList)) :
                    if self.extList[col] == "MGMT VLAN":
                        colValue = chr(col  + 65)
                        searchpat = "MGMT VLAN"
                        break
                self.rowsWritten = self.burnSheet.vlans_subnets_engine.write_MDVO_vlan_info(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname,searchpat,self.sucfilecontent)
                #self.rowsWritten = self.rowsWritten - 1
                if self.rowsWritten < self.max_rows_written :
                    self.rowsWritten = self.max_rows_written
                if self.max_rows_written < self.rowsWritten:
                    self.max_rows_written = self.rowsWritten
                                    
                self.row = self.row  + self.rowsWritten
                
                self.network_attrib_touched = "Yes"

            if self.extList[item] == "Data VLAN"  :
                col = 0
                if self.network_attrib_touched == "Yes" :
                    self.row = self.row  - self.rowsWritten
                
                for col  in range(len(self.extList)) :
                    if self.extList[col] == "Data VLAN" :
                        colValue = chr(col  + 65)
                        searchpat = "DATA VLAN"
                        break
                self.rowsWritten = self.burnSheet.vlans_subnets_engine.write_MDVO_vlan_info(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname,searchpat,self.sucfilecontent)
                #self.rowsWritten = self.rowsWritten - 1
                if self.rowsWritten < self.max_rows_written :
                    self.rowsWritten = self.max_rows_written
                if self.max_rows_written < self.rowsWritten :
                    self.max_rows_written =  self.rowsWritten
                
                
                self.row = self.row  + self.rowsWritten
                self.network_attrib_touched = "Yes"
            
            if  self.extList[item] == "Voice VLAN"  :
                col = 0
                if self.network_attrib_touched == "Yes" :
                    self.row = self.row  - self.rowsWritten
                
                for col  in range(len(self.extList)) :
                    if self.extList[col] ==  "Voice VLAN"  :
                        colValue = chr(col  + 65)
                        searchpat = "VOICE VLAN"
                        break
                self.rowsWritten = self.burnSheet.vlans_subnets_engine.write_MDVO_vlan_info(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname,searchpat,self.sucfilecontent)
                #self.rowsWritten = self.rowsWritten - 1
                if self.rowsWritten < self.max_rows_written :
                    self.rowsWritten = self.max_rows_written
                if self.max_rows_written < self.rowsWritten :
                    self.max_rows_written = self.rowsWritten
                
                self.row = self.row  + self.rowsWritten
                self.network_attrib_touched = "Yes"
               
            if  self.extList[item] == "Wireless VLAN"  :
                col = 0
                if self.network_attrib_touched == "Yes":
                    self.row = self.row  - self.rowsWritten
                
                for col  in range(len(self.extList)) :
                    if self.extList[col] ==  "Wireless VLAN"   :
                        colValue = chr(col  + 65)
                        searchpat = "WIRELESS VLAN all"
                        break
                self.rowsWritten = self.burnSheet.vlans_subnets_engine.write_wireless_vlan_info(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname,self.sucfilecontent)
                #self.rowsWritten = self.rowsWritten - 1
                if self.rowsWritten < self.max_rows_written :
                    self.rowsWritten = self.max_rows_written
                if self.max_rows_written < self.rowsWritten :
                    self.max_rows_written = self.rowsWritten
                
                self.row = self.row  + self.rowsWritten
                self.network_attrib_touched = "Yes"
               
            if  self.extList[item] == "Other VLAN"  :
                col = 0
                if self.network_attrib_touched == "Yes" :
                    self.row = self.row  - self.rowsWritten
                for col  in range(len(self.extList)) :
                    if self.extList[col] ==  "Other VLAN"   :
                        colValue = chr(col  + 65)
                        searchpat = "Misc / Non Standard VLAN"
                        break
                self.rowsWritten = self.burnSheet.vlans_subnets_engine.write_MDVO_vlan_info(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname,searchpat,self.sucfilecontent)
                #self.rowsWritten = self.rowsWritten - 1
                if self.rowsWritten < self.max_rows_written :
                    self.rowsWritten = self.max_rows_written
                if self.max_rows_written < self.rowsWritten :
                    self.max_rows_written = self.rowsWritten
                
                
                self.row = self.row  + self.rowsWritten
                self.network_attrib_touched = "Yes"  
            
            # below section for handling search pattern :
            if  self.extList[item] == "Search Pattern"  :
                col = 0
                if self.search_attrib_touched == "Yes" :
                    self.row = self.row  - self.rowsWritten
                
                for col  in range(len(self.extList)) :
                    if self.extList[col] ==  "Search Pattern"   :
                        colValue = chr(col  + 65)
                        #searchpat = "Misc / Non Standard VLAN"
                        break
        
                self.rowsWritten = self.burnSheet.search_command.write_pattern_info(logpath, ipadd,self.row ,colValue,self.mySheet,self.style,hostnamecol,hostname,self.search_command,self.sucfilecontent,self.orange_style_txt,self.green_style_txt,self.white_style_interface_txt,col)
                
                #self.rowsWritten = self.rowsWritten - 1
                if self.rowsWritten < self.max_rows_written :
                    self.rowsWritten = self.max_rows_written
                if self.max_rows_written < self.rowsWritten :
                    self.max_rows_written = self.rowsWritten
            
                self.row = self.row  + self.rowsWritten
                self.search_attrib_touched = "Yes"  
            
            
            #if self.Auditvartouched == "Y":
            #   self.row = self.row + self.rowsWritte
                
        return self.finalAttrib
            
 
    def writeSheet(self,field):
        
        col =0
        for col in range(len(self.finalAttrib)):
            if self.extList[col] == field:
                
                self.mySheet.write(chr(col+65) + str(self.row),  self.finalAttrib[col], self.style)
            
    