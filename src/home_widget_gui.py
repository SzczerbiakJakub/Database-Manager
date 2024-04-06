from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
import login_gui as login
import descriptions


class HomeWidget(QLabel):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.header = None
        self.login_widget = None
        self.setStyleSheet(" HomeHeaderWidget { border: 1px solid black; }\
                           HomeFooterWidget { border: 1px solid black; }")
        self.build_ui()

    def build_ui(self):
        self.setLayout(self.main_layout)
        self.header = HomeHeaderWidget(self)
        self.main_layout.addWidget(self.header)
        self.body = HomeBodyWidget(self)
        self.main_layout.addWidget(self.body)


class HomeHeaderWidget(QLabel):

    def __init__(self, home_widget):
        super().__init__()
        self.home_widget = home_widget
        self.setFixedHeight(int(home_widget.app.screen_height/5))
        self.main_layout = QHBoxLayout()
        self.setStyleSheet("background-color: rgb(255,251,203);")
        self.build_ui()
        
    def build_ui(self):
        self.setLayout(self.main_layout)
        logo = QPixmap("..\img\logo.png")
        self.setPixmap(logo)


class HomeBodyWidget(QLabel):

    def __init__(self, home_widget):
        super().__init__()
        self.home_widget = home_widget
        self.width = home_widget.app.screen_width
        self.height = int(4*home_widget.app.screen_height/5)
        self.setFixedHeight(self.height)
        self.main_layout = QHBoxLayout()
        self.setStyleSheet("background-color: white;")
        self.build_ui()


    def build_ui(self):
        self.setLayout(self.main_layout)
        
        self.home_widget.login_widget = login.LoginWidget(self, self.home_widget.app)
        self.main_layout.addWidget(self.home_widget.login_widget)
        self.app_description_widget = AppDescriptionWidget(self)
        self.main_layout.addWidget(self.app_description_widget)


class AppDescriptionWidget(QWidget):


    def __init__(self, home_widget_body):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.home_widget_body = home_widget_body
        self.main_description_widget = None
        self.key_description_widget = None
        self.width = int(4*self.home_widget_body.width/5)
        self.height = home_widget_body.height
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        
        self.build_ui()

    def build_ui(self):
        self.setLayout(self.main_layout)
        self.build_description_widgets()

    def build_description_widgets(self):
        self.main_description_widget = descriptions.MainDescritpionWidget(self)
        self.main_layout.addWidget(self.main_description_widget)
        palceholder = descriptions.Placeholder(self)
        self.main_layout.addWidget(palceholder)
        

    



