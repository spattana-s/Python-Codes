'''
Created on 2 June  2018

@author: sp977u@att.com  (Satish Palnati)

'''
from PySide import QtGui
from PySide import QtCore
from views.common.left_base_view import left_base

class push_controls:

    def __init__(self,gui,left_common):
        
        self.gui = gui
    
        self.left_common = left_common
        
    
    def display_push(self):
    
        self.left_common.last_parent.credentials_groupbox.show()
        self.left_common.last_parent.IP_groupBox.show()
        self.left_common.last_parent.Commands_groupBox.show()
        self.left_common.last_parent.results_groupBox.show()
        
        self.left_common.show_left_common()
        self.left_common.cr_box.show()
        self.left_common.cr_label.show()
   
        self.left_common.go_button.show()
        self.left_common.go_button.setText("Push")
        
    def hide_push(self):
        
        self.left_common.cr_box.hide()
        self.left_common.cr_label.hide()
              
        
        