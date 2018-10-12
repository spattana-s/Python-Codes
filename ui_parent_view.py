'''
Created on 20 May, 2018

@author: sp977u@att.com  (Satish Palnati)

'''
from PySide import QtGui
from PySide import QtCore
import os
import logos
from PySide.QtCore import Signal
from PySide.QtGui import QWidget,QFrame, QHBoxLayout, QVBoxLayout, QMainWindow, QLabel
from views.common.extract_view import extract_excel
from views import validate_inputs
from views.common.left_base_view import left_base
from views.common.get_view import get_controls
from views.common.push_view import push_controls
from views.common.compare_view import compare_op_results
import time
from asyncio.tasks import sleep

class Ui_MainView(QMainWindow):
    
    gui_methods_sig =  Signal(int,)
        
    def __init__(self,):
        super(Ui_MainView, self).__init__()
        
        self.output_folder = os.getcwd()
        self.usr = ''
        self.psw = ''
        
        self.save_username_checked = False
        
        self.right_base_layout_v = QtGui.QVBoxLayout()
        self.msgBox = QtGui.QMessageBox()
        
        self.validations = validate_inputs.validate_controls(self) # instance for input validations  and we are passing self to validate class for model updations
       
    def gifUI(self,gui_slate):
       
        self.gui = gui_slate
        self.gif_widget = QWidget()
        self.gif_layout = QVBoxLayout()
        
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)        
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        self.gif_layout.addWidget(self.movie_screen)
                                           
        ag_file = "GIF-180704_103026.gif"
        
        self.movie = QtGui.QMovie(ag_file, QtCore.QByteArray(), self.gif_widget) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.setSpeed(75) 
        self.movie_screen.setMovie(self.movie)
#         self.movie_screen.setFixedWidth(500)
        
        self.gif_widget.setLayout(self.gif_layout)
        self.gui.setCentralWidget(self.gif_widget)
#         self.gui.addDockWidget(self.gif_widget)
        self.movie.start()
#         self.movie.setPaused(True)
        self.gif_widget.show()
#         time.sleep(2)
#         self.movie.stop()

       
            
    def setupUi(self,gui_slate):
        
        self.gui = gui_slate
        self.gui.get_option_selected = False
        self.gui.push_option_selected = False
        self.gui.extract_opt_selected = False
        self.gui.compare_opt_selected = False
        
#Outer most Main Layout        
   
        self.widget = QWidget()
        self.widget.setMinimumSize(850,600)

        self.main_layout_h = QHBoxLayout()
        self.main_layout_h.setAlignment(QtCore.Qt.AlignTop)
        
        self.widget.setLayout(self.main_layout_h)
        
        self.gui.setCentralWidget(self.widget)
        
        self.left_base_widget = QWidget()
#         self.left_base_widget.setMaximumWidth(600)
#         self.left_base_widget.setMinimumWidth(450)
#         self.left_base_widget.setMaximumHeight(700)
        
        self.right_base_widget = QWidget()
        
#3 Sub main Layouts
        
        self.left_base_layout_v = QVBoxLayout()
#         self.right_base_layout_v = QVBoxLayout()
        self.corner_logo_layout_v = QVBoxLayout()
        self.left_base_layout_v.setAlignment(QtCore.Qt.AlignTop)
        
        self.right_base_layout_v.setAlignment(QtCore.Qt.AlignTop)
                
#Added Widgets and layouts to the outermost layout

        self.main_layout_h.addWidget(self.left_base_widget)
        self.main_layout_h.addWidget(self.right_base_widget)
        self.main_layout_h.addLayout(self.corner_logo_layout_v)
        
#         , QtGui.QFont.Normal
        self.grp_heading_font = QtGui.QFont("Verdana", 10)
        self.grp_heading_font.setItalic(True)
        
#Radio buttons layout 

        self.radio_groupBox = QtGui.QGroupBox()
        self.radio_option_layout_lb_h = QHBoxLayout()
        
        self.radio_groupBox.setLayout(self.radio_option_layout_lb_h)
        
        self.radio_groupBox.setMinimumWidth(450)
        self.left_base_layout_v.addWidget(self.radio_groupBox)
        
#Credentials layouts     

        self.credentials_groupbox = QtGui.QGroupBox("GTAC Credentials")
        self.credentials_groupbox.setFont(self.grp_heading_font)
        self.credentials_layout_lb_v = QVBoxLayout()
        
        self.username_layout_lb_h = QHBoxLayout()
        self.password_layout_lb_h = QHBoxLayout()
        self.cr_layout_lb_h = QHBoxLayout()
        self.password_layout_lb_h.setAlignment(QtCore.Qt.AlignLeft)
        self.credentials_layout_lb_v.addLayout(self.username_layout_lb_h)
        self.credentials_layout_lb_v.addLayout(self.password_layout_lb_h)
        self.credentials_layout_lb_v.addLayout(self.cr_layout_lb_h)
        
        self.credentials_groupbox.setLayout(self.credentials_layout_lb_v)
        self.left_base_layout_v.addWidget(self.credentials_groupbox)
        self.credentials_groupbox.setAlignment(QtCore.Qt.AlignLeft)
        self.credentials_groupbox.hide()

#IP group box layouts
        
        self.IP_groupBox = QtGui.QGroupBox("IP Inputs")
        self.IP_groupBox.setFont(self.grp_heading_font)
        self.ip_file_layout_lb_v = QVBoxLayout()
        
        self.ip_file_select_layout_lb_h = QHBoxLayout()
        self.ip_file_select_layout_lb_h.setAlignment(QtCore.Qt.AlignLeft)
        self.ip_file_layout_lb_v.addLayout(self.ip_file_select_layout_lb_h)
        
        self.IP_groupBox.setMaximumHeight(135)
        self.IP_groupBox.setLayout(self.ip_file_layout_lb_v)
        self.left_base_layout_v.addWidget(self.IP_groupBox)
        
        self.IP_groupBox.hide()
        
# Commands  group box selection

        self.Commands_groupBox = QtGui.QGroupBox("Commands Inputs") 
        self.Commands_groupBox.setFont(self.grp_heading_font)
        self.commands_label_layout_lb_v = QVBoxLayout()
        
        self.default_chkbx_layout_lb_h = QHBoxLayout()
        self.commands_file_layout_lb_h = QHBoxLayout()
        self.commands_file_layout_lb_h.setAlignment(QtCore.Qt.AlignLeft)
        self.commands_custom_box_layout_lb_h = QHBoxLayout()
        self.none_radio_btn_layout_lb_h = QHBoxLayout()
        
        self.commands_label_layout_lb_v.addLayout(self.default_chkbx_layout_lb_h)
        self.commands_label_layout_lb_v.addLayout(self.commands_file_layout_lb_h)
        self.commands_label_layout_lb_v.addLayout(self.commands_custom_box_layout_lb_h)
        self.commands_label_layout_lb_v.addLayout(self.none_radio_btn_layout_lb_h)

        self.Commands_groupBox.setMaximumHeight(225)
        self.Commands_groupBox.setAlignment(QtCore.Qt.AlignLeft)
        self.Commands_groupBox.setLayout(self.commands_label_layout_lb_v)
        self.left_base_layout_v.addWidget(self.Commands_groupBox)
        
        self.Commands_groupBox.hide()
        
# results group box 

        self.results_groupBox = QtGui.QGroupBox("Results")
        self.results_groupBox.setFont(self.grp_heading_font)
        self.results_layout_lb_v = QVBoxLayout() 

        self.output_layout_lb_h = QHBoxLayout()
        self.output_layout_lb_h.setAlignment(QtCore.Qt.AlignLeft)
        
        self.results_layout_lb_v.addLayout(self.output_layout_lb_h)

        self.results_groupBox.setLayout(self.results_layout_lb_v)
        self.left_base_layout_v.addWidget(self.results_groupBox)
               
        self.results_groupBox.hide()
         
# Go Button 
        
        self.go_btn_layout_lb_h = QHBoxLayout()
        self.left_base_layout_v.addLayout(self.go_btn_layout_lb_h)        

# Right and Left Widget on individual layouts
       
        self.left_base_widget.setLayout(self.left_base_layout_v)
        self.right_base_widget.setLayout(self.right_base_layout_v) 
        
#### just to see right base layout 
        
        self.right_base = QtGui.QTextEdit(self.gui)
        self.right_base.setStyleSheet("""QToolTip { background-color: #00bfff; color: black; border: black solid 2px  }""")
        self.right_base.setObjectName("IP_Address")
        self.right_base_layout_v.addWidget(self.right_base)
#         self.right_base.setMaximumHeight(500)
        self.right_base.hide()
        
        self.snap_gif = QtGui.QLabel(self.gui)
        self.snap_gif.setText("")
        self.snap_gif.setStyleSheet("background-color: None")
        self.snap_gif.setPixmap(QtGui.QPixmap("Capture.png"))
        self.snap_gif.setObjectName("logo_corner")
        self.right_base_layout_v.addWidget(self.snap_gif) 
        
        
######
   
        self.gui.setWindowTitle('SPEED +  3.0')
        self.gui.setWindowIcon(QtGui.QIcon(":/logo/Wind_icon.png"))
        self.gui.setAutoFillBackground(True)
        
        self.corner_logolabel = QtGui.QLabel(self.gui)
        self.corner_logolabel.setText("")
        self.corner_logolabel.setStyleSheet("background-color: None")
        self.corner_logolabel.setPixmap(QtGui.QPixmap(":/logo/ATT-LOGO-2.png"))
        self.corner_logolabel.setObjectName("logo_corner")
#         self.corner_logo_layout_v.setAlignment(QtCore.Qt.AlignTop)
        self.corner_logo_layout_v.setAlignment(int(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight))
        self.corner_logo_layout_v.addWidget(self.corner_logolabel)    
        
        
        self.msgBox.setWindowIcon(QtGui.QIcon(":/logo/Wind_icon.png"))
        self.msgBox.setFont(QtGui.QFont("Verdana", 8, QtGui.QFont.Normal))
        self.make_menu()
## gif at&t logo        
#         self.movie_screen = QLabel()
#         self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)        
#         self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
#         self.right_base_layout_v.addWidget(self.movie_screen)
#                                            
#         ag_file = "C:/Users/rg012f/eclipse-workspace/poojan_try/giphy.gif"
#         self.movie = QtGui.QMovie(ag_file, QtCore.QByteArray(), None) 
#         self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
#         self.movie.setSpeed(75) 
#         self.movie_screen.setMovie(self.movie)
# 
#         
#         self.movie.setPaused(True)
#         self.movie.start()
#         self.right_base_widget.show()
#         time.sleep(2)

######################### order of the below funtion calls is importnant change them wisely#####################
        self.check_save_username()
        self.create_views()
        self.left_radio_controls()
        self.connect_child_views()
        
    def make_menu(self):
        self.myMenu = self.gui.menuBar()
          
        self.file = self.myMenu.addMenu('&File')
          
        self.file.addAction("&Select Output Folder...",self.select_destination, "Ctrl+O")
        self.file.addAction("&Exit",self.closewindow, "Ctrl+X")
          
        self.file = self.myMenu.addMenu('&Help')
          
        self.file.addAction("&About...",self.about_tool, "Ctrl+H")
        
    def check_save_username(self):
        print("Yo reached save username")
        try:
            f = open('Username.txt','r')
            lines = f.readlines()
            if len(lines):
                self.save_username_checked = True
            else:
                self.save_username_checked = False
        except Exception as ex:
            print(ex)
        
        
         
    def select_destination(self, ):
        
        fld = QtGui.QFileDialog.getExistingDirectory(self.gui, 'Select Output Folder')
        self.output_folder = str(fld)
        
        
    def closewindow(self):
        self.gui.close()
        
    def about_tool(self):
        abouttool = "Speed + v3.0 \n\nThis tool is useful to fetch, push, extract, compare device configs \n"
        
        self.msgBox.setText(abouttool)
        self.msgBox.setWindowTitle("About Speed +")
        self.msgBox.show()
    
    def left_radio_controls(self):
        
# ============================    main radio options selection :
        radio_font = QtGui.QFont("Verdana", 10, QtGui.QFont.Normal)
        
        self.get_radio_option =  QtGui.QRadioButton(self.gui)
        self.get_radio_option.setFont(radio_font)
        self.get_radio_option.setText("Get")
        self.radio_option_layout_lb_h.addWidget(self.get_radio_option)
        
        self.push_radio_option =  QtGui.QRadioButton(self.gui)
        self.push_radio_option.setFont(radio_font)
        self.push_radio_option.setText("Push")
        self.radio_option_layout_lb_h.addWidget(self.push_radio_option)
        
        self.extract_radio_option =  QtGui.QRadioButton(self.gui)
        self.extract_radio_option.setFont(radio_font)
        self.extract_radio_option.setText("Extract")
        self.radio_option_layout_lb_h.addWidget(self.extract_radio_option)
        
        self.compare_radio_option =  QtGui.QRadioButton(self.gui)
        self.compare_radio_option.setFont(radio_font)
        self.compare_radio_option.setText("Compare")
        self.radio_option_layout_lb_h.addWidget(self.compare_radio_option)
        
    def disp_get_options(self):
        
        self.snap_gif.show()
        self.push_view.hide_push()
        self.excel_view.userOptionextract.hide()
        self.compare_view.main_widget.hide()
        self.get_view.display_get()
        
    def disp_push_options(self):
        
        self.snap_gif.show()
        self.get_view.hide_get()
        self.excel_view.userOptionextract.hide()
        self.compare_view.main_widget.hide()
        self.push_view.display_push()
        self.validations.hide_right_common()
        
    def disp_ext_options(self):
        
        self.get_view.hide_get()
        self.push_view.hide_push()
        self.compare_view.main_widget.hide()
        self.excel_view.display_excel_portion()
        self.validations.hide_right_common()
        
    def disp_comp_options(self):
        
        self.get_view.hide_get()
        self.push_view.hide_push()
        self.excel_view.userOptionextract.hide()
        self.compare_view.display_comapre_portion()
        self.validations.hide_right_common()
        
    def connect_child_views(self):
        
        self.get_radio_option.clicked.connect(self.disp_get_options)
        self.push_radio_option.clicked.connect(self.disp_push_options)
        self.extract_radio_option.clicked.connect(self.disp_ext_options)
        self.compare_radio_option.clicked.connect(self.disp_comp_options)
        
        self.base_left.go_button.clicked.connect(self.connect_validate_option)
    
    def connect_validate_option(self):
        
        self.validations.validate_user_inputs() # passing self to validation class method , other end this self is last_parent
        
    def create_views(self):
        
        self.base_left = left_base(self)  # we are passing main GUI and also local self as 'last_parent' to left base view to update variables
        
        self.get_view = get_controls(self.gui,self.base_left)
        self.push_view = push_controls(self.gui,self.base_left)
        self.excel_view = extract_excel(self.gui,self.base_left)
        self.compare_view = compare_op_results(self)
        
    def show_gif_right_base(self,path,layout):
        print("ui parent view show_gif_right_base line 394")
        self.movie_screen = QLabel()
        self.movie_screen.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)        
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.movie_screen)
                                            
        ag_file = path
        self.movie = QtGui.QMovie(ag_file, QtCore.QByteArray(), None) 
        self.movie.setCacheMode(QtGui.QMovie.CacheAll) 
        self.movie.setSpeed(75) 
        self.movie_screen.setMovie(self.movie)
 
        #"C:/Users/rg012f/eclipse-workspace/poojan_try/giphy.gif"
        self.movie.setPaused(True)
        self.movie.start()
#         self.right_base_widget.setLayout(layout)
#         self.right_base_widget.show()

    def hide_gif_right_base(self):
        self.movie_screen.hide()
        