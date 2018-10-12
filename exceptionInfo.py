'''
Created on 8  NOV 2017

@author: sp977u ( Satish Palnati )
'''

class exceptionDetails :
    
    def doIhaveExceptioinInfo(self,logpath, ipadd):
        
        self.Final = "NF"
        self.serialList = []
        self.rowswritten = 0
        self.juniScan = "N"
        self.exceptionInfo = " "
        self.logpath = logpath
        self.ipadd = ipadd
        self.tempBanner = "NF"
        
        try :
            self.sucFile = open(logpath + "\\" + ipadd + ".txt" , 'r')
            
            while 1:
                self.line = self.sucFile.readline()
                
                if "show" in self.line or "sho" in self.line :
                    continue
                if "banner " in self.line :
                    self.tempBanner = (self.line [ : ]).lower()
                    if "EXCEPTION" in self.tempBanner or "exception" in self.tempBanner :
                        self.Final = "Yes"
                        loc1 = self.tempBanner.find("exception")
                        self.exceptionInfo = (self.line[loc1:]).replace("*** ^",'')
                        self.exceptionInfo = self.exceptionInfo.replace("*** ^C",'')
                        self.exceptionInfo = self.exceptionInfo.replace('\n','')
                    break
                
                if "announcement" in  self.line  :
                    self.tempBanner = (self.line [ : ]).lower()
                    
                    if "exception" in self.tempBanner :
                        self.Final = "Yes"
                        loc1 = self.tempBanner.find("exception")
                        self.exceptionInfo = (self.line[loc1:]).replace("***",'')
                        self.exceptionInfo = self.exceptionInfo.replace("\n", '')
                    break
            
        
                if not self.line:
                    break
                if self.line =="\n":
                    continue
            self.sucFile.close()
            #print( partNoList)
            return self.Final,self.exceptionInfo
            
        except Exception as ex:
            print(ex)
            self.sucFile.close()
            return "Fail",self.exceptionInfo
    #===
