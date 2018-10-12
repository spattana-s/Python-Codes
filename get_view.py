'''
Created on 2 June  2018

Remove gui variable if it is not not required as we are using from left base view

@author: sp977u@att.com  (Satish Palnati)

'''
from PySide import QtGui
from PySide import QtCore
from views.common.left_base_view import left_base


class get_controls:

    def __init__(self,gui,left_common):
        
        self.gui = gui
        self.left_common = left_common
        #super(left_base,self).__init__()
        
        #self.create_get_specific()
        
        

    def display_get(self):
        
        self.left_common.show_left_common()
        
        self.left_common.last_parent.credentials_groupbox.show()
        self.left_common.last_parent.IP_groupBox.show()
        self.left_common.last_parent.Commands_groupBox.show()
        self.left_common.last_parent.results_groupBox.show()
        
        
        self.left_common.get_conf_logs_chbx.show()
        self.left_common.get_config_flatfile_chbx.show()
        self.left_common.get_ping_logs_chbx.show()
        
        self.left_common.go_button.show()
        self.left_common.go_button.setText("Get")
        
    def hide_get(self):
        
        self.left_common.get_conf_logs_chbx.hide()
        self.left_common.get_ping_logs_chbx.hide()
        self.left_common.default_commands_chbx.hide()
        self.left_common.get_config_flatfile_chbx.hide()
        
        
        
        
        
              
    