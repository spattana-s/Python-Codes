'''
Created on Apr 28, 2017

@author: sp977u
'''


class partNoNameauditTab :
    
    def getPartnoInfo(self,logpath, ipadd, row,column, mySheet,style,hostnamecol,hsname):
        
        Final = "NF"
        partNoList = []
        rowswritten = 0
        juniScan = "N"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if "PID" in line :
                    loc = line.find(',')
                    Final  =  line[ : loc ]
                    Final = Final.replace("PID:", ' ')
                    Final = Final.strip()
                    
                    partNoList.append(Final)
                    
                    temprow = str(row)
                    mySheet.write(hostnamecol + temprow , hsname, style)
                    mySheet.write(column + str(temprow),  Final, style)
                    row = row + 1
                    rowswritten = rowswritten + 1
                
                if "Item" in line and "Version" in line and "Part number" in line and "Serial number" in line and "Description" in line:
                    juniScan = "Y"
                    loc1 = line.find("Part number")
                    loc2 = line.find("Serial")
                    line = sucFile.readline()
                if juniScan == "Y":
                    
                    if not line or line == "\n":
                        break
                    
                    Final  =  line[loc1 : loc2 ]
                    Final = Final.strip()
                    
                    partNoList.append(Final)
                    
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
            return partNoList, rowswritten
            
        except Exception as ex:
            print(ex)
            sucFile.close()
            return "NF",rowswritten
    #=======================================================================================================
    def getPartnameInfo(self,logpath, ipadd, row,column, mySheet,style,hostnamecol,hsname):
        
        Final = "NF"
        partNameList = []
        rowswritten = 0
        juniScan = "N"
        try :
            sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                line = sucFile.readline()
                if ("NAME:" in line and "DESCR:" in line ) or ("Name:" in line and "DESCR:" in line ) :
                    loc = line.find(',')
                    Final  =  line[ : loc ]
                    
                    Final = Final.replace('"', " ")
                    
                    Final = Final.replace("NAME:", ' ')
                    Final = Final.replace("Name:", " ")
                    Final = Final.strip()
                    
                    partNameList.append(Final)
                    
                    temprow = str(row)
                    mySheet.write(hostnamecol + temprow , hsname, style)
                    mySheet.write(column + str(temprow),  Final, style)
                    row = row + 1
                    rowswritten = rowswritten + 1
                
                if "Item" in line and "Version" in line and "Part number" in line and "Serial number" in line and "Description" in line:
                    juniScan = "Y"
                    loc1 = line.find("Item")
                    loc2 = line.find("Version")
                    line = sucFile.readline()
                if juniScan == "Y":
                    
                    if not line or line == "\n":
                        break
                    
                    Final  =  line[loc1 : loc2 ]
                    Final = Final.strip()
                    
                    partNameList.append(Final)
                    
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
            return partNameList, rowswritten
            
        except Exception as ex:
            print(ex)
            sucFile.close()
            return "NF",rowswritten
        
        