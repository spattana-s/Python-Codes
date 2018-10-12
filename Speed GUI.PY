from PySide import QtGui
import sys
from views.master_view import MasterView
#from PySide.QtGui import QApplication

import logos


class Speed_App(QtGui.QApplication):
    
    def __init__(self, sys_argv):
        super(Speed_App, self).__init__(sys_argv)
        #self.model = Model()
        #self.main_ctrl = MainController(self.model)
        #self.main_view = MainView(self.model, self.main_ctrl)
        self.parent_view = MasterView()
        self.parent_view.show()
        
        
        
    
if __name__ == '__main__':
    
    app = Speed_App(sys.argv)
    
    sys.exit(app.exec_())
    
    

    
