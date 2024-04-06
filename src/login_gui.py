from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
import sql_handler as sql_handler
import descriptions



class LoginWidget(QLabel):

    def __init__(self, home_widget_body, app):
        super().__init__()
        self.home_widget_body = home_widget_body
        self.app = app
        self.width = int(home_widget_body.width/5)
        self.height = home_widget_body.height
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.login_panel = None
        self.host_entry = None
        self.username_entry = None
        self.password_entry = None
        self.port_entry = None
        self.main_layout = QVBoxLayout()
        self.setStyleSheet("background-color: rgb(255,251,203);")
        self.build_login_widget()
        

    def build_login_widget(self):
        self.setLayout(self.main_layout)
        self.login_panel = LoginPanel(self)
        self.main_layout.addWidget(self.login_panel)
        key_fetures_description = descriptions.KeyDescritpionWidget(self)
        self.main_layout.addWidget(key_fetures_description)
        placeholder = descriptions.Placeholder(self)
        self.main_layout.addWidget(placeholder)
        


    


    def login(self):
        params_db = {}
        params_db["host"] = self.login_panel.host_row.host_entry.text()
        params_db["user"] = self.login_panel.username_row.username_entry.text()
        params_db["password"] = self.login_panel.password_row.password_entry.text()
        params_db["port"] = self.login_panel.port_row.port_entry.text()
        self.try_to_log_in(params_db)
        
        

    def try_to_log_in(self, params):
        connection = sql_handler.DBManager.login_connect(params)
        if connection:
            self.accept_login_trial(params)
        else:
            self.deny_login_trial()

    def accept_login_trial(self, params):
        self.app.db_manager = sql_handler.DBManager(self.app, params)
        self.app.build_db_management_widget(params["user"])
        self.app.main_widget.setCurrentIndex(1)

    def deny_login_trial(self):
        self.app.raise_error(e="login_error", function=None, parameters=None, row_number=None, database_name=None)


class LoginPanel(QLabel):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.width = int(9*self.parent.width/10)
        self.height = int(self.parent.height/3)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setStyleSheet("border: 1px solid black; background-color: white; ")
        self.layout = QVBoxLayout()
        self.host_row = None
        self.username_row = None
        self.password_row = None
        self.port_row = None
        self.login_button = None
        self.build_panel()

    def build_panel(self):
        self.setLayout(self.layout)
        self.host_row = HostRow(self)
        self.layout.addWidget(self.host_row)
        self.username_row = UsernameRow(self)
        self.layout.addWidget(self.username_row)
        self.password_row = PasswordRow(self)
        self.layout.addWidget(self.password_row)
        self.port_row = PortRow(self)
        self.layout.addWidget(self.port_row)
        self.login_button = QPushButton("Login")
        self.login_button.setFixedHeight(30)
        self.login_button.clicked.connect(self.parent.login)
        self.layout.addWidget(self.login_button)





class HostRow(QLabel):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.setStyleSheet("border: none; ")
        self.build_host_row()

    def build_host_row(self):
        self.setLayout(self.layout)
        self.host_label, self.host_entry = QLabel("Host: "), QLineEdit("localhost")
        self.host_entry.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.host_label)
        self.layout.addWidget(self.host_entry)

class UsernameRow(QLabel):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.setStyleSheet("border: none; ")
        self.build_username_row()

    def build_username_row(self):
        self.setLayout(self.layout)
        self.username_label, self.username_entry = QLabel("Username: "), QLineEdit("postgres")
        self.username_entry.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_entry)

class PasswordRow(QLabel):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.setStyleSheet("border: none; ")
        self.build_password_row()

    def build_password_row(self):
        self.setLayout(self.layout)
        self.password_label, self.password_entry = QLabel("Password: "), QLineEdit("admin")
        self.password_entry.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_entry)

class PortRow(QLabel):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.setStyleSheet("border: none; ")
        self.build_port_row()

    def build_port_row(self):
        self.setLayout(self.layout)
        self.port_label, self.port_entry = QLabel("Port: "), QLineEdit("5432")
        self.port_entry.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.port_label)
        self.layout.addWidget(self.port_entry)



