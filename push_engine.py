'''
Created on Jul 11, 2018

@author: rg012f
'''
from PySide import QtCore,QtGui
import os 
import time
import datetime
import threading
from service_network.device_wheels.CommandProcessor import CommandProcessor
from service_network.device_wheels.MyProgressBar import MyProgressBar
from views.push_window.push_window import PushWindow

class PushEngine:
    
    quit_flag = False

    def __init__(self,common_model,last_parent):
        self.common_model = common_model
        self.signalcount = 0
        self.threadPool = QtCore.QThreadPool()
        self.lock = threading.Lock()
        self.threadPool.setMaxThreadCount(1)
    
        self.last_parent =  last_parent
        self.progress = MyProgressBar( len(self.common_model.final_ip_list))
        self.push_window = PushWindow(last_parent)
        
    def start_push_engine(self):
        
        print("yo reached here")
        self.push_window.prepare_window()
        
        