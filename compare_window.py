'''
Created on Jul 11, 2018

@author: rg012f
'''
import sys
from PySide.QtGui  import * 
from PySide.QtCore import *
from PySide import QtGui
from PySide import QtCore
import os

class CompareWindow:

    wind_close_flg = False

    def __init__(self,last_parent):
        
        print("reached init of Compare Window")
        
        #pop ka code idhar daalna hai
        
    def prepare_window(self,):
        print("reached prepare window")
    
    def closeEvent(self,event):
        
       
        self.wind_close_flg = True