'''
Created on OCT 24, 2017

@author: sp977u@att.com  (Satish Palnati)

This class is base window for application.

'''
from PySide.QtGui import QMainWindow
from views.common.ui_parent_view import Ui_MainView
from PySide.QtCore import Signal
from views import validate_inputs
import time

class MasterView(QMainWindow):



    # properties to read/write widget value
    @property
    def running(self):
        return self.ui.pushButton_running.isChecked()
    @running.setter
    def running(self, value):
        self.ui.pushButton_running.setChecked(value)

    def __init__(self,):
        #self.model = model
        #self.main_ctrl = main_ctrl
        super(MasterView, self).__init__()
        self.build_base_ui()
        
    
        # register func with model for future model update announcements
        #self.model.subscribe_update_func(self.update_ui_from_model)

    def build_base_ui(self):
        self.ui = Ui_MainView()  # instance for UI creation
#         self.ui.gifUI(self)
        self.ui.setupUi(self)
        
         
        print("Testing for UI build")
        
        # connect signal to method 
        #self.ui.pushButton_running.clicked.connect(self.on_running)
