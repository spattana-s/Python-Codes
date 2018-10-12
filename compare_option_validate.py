'''
Created on Jul 11, 2018

@author: rg012f
'''
class validate_compare_opt:

    def __init__(self,last_parent,common_model,model_compare):
        
        self.last_parent = last_parent
        self.common_model = common_model
        self.model_compare = model_compare
    
    def kick_compare_view_validations(self):
        self.ip_box_cnt = self.last_parent.base_left.ip_add_box.toPlainText()
        self.command_box_cnt = self.last_parent.base_left.commands_box.toPlainText()
#         self.cr_number = self.last_parent.base_left.cr_box.toPlainText()
        print("comapre validations here")
