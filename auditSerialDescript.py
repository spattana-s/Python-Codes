'''
Created on Apr 28, 2017

@author: sp977u
'''


class auditSerial_Description :
    
    def getauditSerialnoInfo(self,logpath, ipadd, row,column, mySheet,style,hostnamecol,hsname):
        
        Final = "NF"
        serialList = []
        rowswritten = 0
        juniScan = "N"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if "PID" in line and "SN:" in line :
                    
                    loc = line.find('SN:')
                    Final  =  line[ loc : ]
                    Final = Final.strip()
                    Final = Final.replace("SN:", ' ')
                    
                    serialList.append(Final)
                    
                    temprow = str(row)
                    mySheet.write(hostnamecol + temprow , hsname, style)
                    mySheet.write(column + str(temprow),  Final, style)
                    row = row + 1
                    rowswritten = rowswritten + 1
                
                if "Item" in line and "Version" in line and "Part number" in line and "Serial number" in line and "Description" in line:
                    juniScan = "Y"
                    loc1 = line.find("Serial number")
                    loc2 = line.find("Description")
                    line = sucFile.readline()
                if juniScan == "Y":
                    
                    if not line or line == "\n":
                        break
                    
                    Final  =  line[loc1 : loc2 ]
                    Final = Final.strip()
                    
                    serialList.append(Final)
                    
                    temprow = str(row)
                    mySheet.write(hostnamecol + temprow , hsname, style)
                    mySheet.write(column + str(temprow),  Final, style)
                    row = row + 1
                    rowswritten = rowswritten + 1
                    
                
                if not line:
                    break
                if line =="\n":
                    continue
            sucFile.close()
            #print( partNoList)
            return serialList, rowswritten
            
        except Exception as ex:
            print(ex)
            sucFile.close()
            return "NF",rowswritten
    #=======================================================================================================
    def getDescriptionInfo(self,logpath, ipadd, row,column, mySheet,style,hostnamecol,hsname):
        
        Final = "NF"
        descriList = []
        rowswritten = 0
        juniScan = "N"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if ("NAME:" in line and "DESCR:" in line ) or ("Name:" in line and "DESCR:" in line ) :
                    loc = line.find('DESCR')
                    Final  =  line[ loc :  ]
                    
                    Final = Final.replace('"', " ")
                    Final = Final.replace("DESCR:", ' ')
                    Final = Final.strip()
                    
                    descriList.append(Final)
                    
                    temprow = str(row)
                    mySheet.write(hostnamecol + temprow , hsname, style)
                    mySheet.write(column + str(temprow),  Final, style)
                    row = row + 1
                    rowswritten = rowswritten + 1
                if "Item" in line and "Version" in line and "Part number" in line and "Serial number" in line and "Description" in line:
                    juniScan = "Y"
                    loc1 = line.find("Description")
                    
                    line = sucFile.readline()
                if juniScan == "Y":
                    
                    if not line or line == "\n":
                        break
                    
                    Final  =  line[loc1 : ]
                    Final = Final.strip()
                    
                    descriList.append(Final)
                    
                    temprow = str(row)
                    mySheet.write(hostnamecol + temprow , hsname, style)
                    mySheet.write(column + str(temprow),  Final, style)
                    row = row + 1
                    rowswritten = rowswritten + 1
                 
                    
                if not line:
                    break
                if line =="\n":
                    continue
            sucFile.close()
            #print( partNoList)
            return descriList, rowswritten
            
        except Exception as ex:
            print(ex)
            sucFile.close()
            return "NF",rowswritten
        
        