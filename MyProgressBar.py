#import sys

#import re
#import os
#import time
import datetime
#import logging
import threading

#import os.path
#from threading import Thread, Event

class MyProgressBar:

    def __init__(self,totalCount):
        self.counter=0
        self.lock = threading.Lock()
        #self._sentinel = _sentinel 
        self.totalCount = totalCount
        
        
        self.evt= threading.Event()
        self.Fail_Final = []
        self.Duplicates = []
        #self.evt = evt
        self.startTime = datetime.datetime.now().replace(microsecond=0)
    #def updateProgressBar(self,ipaddress,Final_log_path,evt): 
    def updateProgressBar(self,ipaddress,Final_log_path,status,Phs,DupeFlg):
        self.lock.acquire()
        self.counter = self.counter + 1
        self.JobDone = 'F'
        
        #self.config_file =os.getcwd() + "\\Logs\\" + ipaddress +".txt"
        self.phase = Phs
        self.DupeFlag = DupeFlg
        #self.DupeIP = DupIP
        #print " I have reached update progress..."
        #self._sentinel = _sentinel
        #logFile.write("Processing completed for the ipaddress : "+str(ipaddress)+"\n")
        
        print("Current total count : ",self.totalCount)
        
        if (status == True and  self.phase == 1 ) or ( status == True and self.phase == 2) :
            self.final_log_file = open(Final_log_path +"\\Final_log.txt","a+")
            self.final_log_file.write(str(ipaddress) + "  : Success \n")
            self.final_log_file.close()
            self.JobDone = "T"
            print("\nProcessing completed "+str(self.counter) + "/" + str(self.totalCount)+" for the ipaddress : "+str(ipaddress)+"\n")
            #self.out_q.put(self.JobDone)
            #self.out_q.put((self.JobDone,self.evt))
            #print "\n Iam in waiting mode "
            #self.out_q.put(self.counter)
            #self.evt.wait()
        elif status == False and self.phase ==2:
            self.JobDone ="FF"
            #self.final_log_file = open(Final_log_path +"\\Final_log.txt","a+")
            #self.final_log_file.write(str(ipaddress) + "  : Fail \n")
            #self.final_log_file.close()
            
            #print"\n Fail finally...! "+str(ipaddress)
            #print "\n Iam in waiting mode  , "
            #self.out_q.put(self.counter)
            if self.DupeFlag == "Y":
                #self.Duplicates.append(self.DupeIP)
                pass
            else :
                
                self.Fail_Final.append(ipaddress)
            print("\nProcessing completed "+str(self.counter) + "/" + str(self.totalCount)+" for the ipaddress : "+str(ipaddress)+"\n")
        
        elif status == False and self.phase ==1:
            if self.DupeFlag == "N":
                
                #print"\nCouter : "+str(self.counter)
                #print "Second round attempt for the device :" +str(ipaddress)
                self.counter = self.counter - 1
                #print"\nCouter : "+str(self.counter)
            elif self.DupeFlag == "Y":
                #self.Duplicates.append(self.DupeIP)
                print("\nProcessing completed "+str(self.counter) + "/" + str(self.totalCount)+" for the ipaddress : "+str(ipaddress)+"\n")
        
        last_counter = self.counter      
        
        if self.totalCount == self.counter :
            
            endTime = datetime.datetime.now().replace(microsecond=0)            
            timeTaken = endTime - self.startTime
            self.final_log_file = open(Final_log_path +"\\Final_log.txt","a+")
            self.final_log_file.write("\n")
            for fl in self.Fail_Final:
                self.final_log_file.write(str(fl) + "  : Fail \n")
            self.final_log_file.write("\n\n")
            for dp in self.Duplicates:
                self.final_log_file.write(str(dp) + "  : Duplicate IP\n")
            
            #self.final_log_file = open(Final_log_path +"\\Final_log.txt","a+")
            self.final_log_file.write("\n\n\nTotal Time Taken for Backup process : "+str(timeTaken) )
            self.final_log_file.write(" Seconds\n")
            self.final_log_file.close()
            self.counter = 0
            
            self.Fail_Final.clear()
            self.Duplicates.clear()
            
            
            #self.out_q.put(self.counter)
            
            print ("\nTotal TimeTaken to complete " + str(self.totalCount) +" Jobs : "+str(timeTaken))
                       
        self.lock.release()
        return last_counter
            