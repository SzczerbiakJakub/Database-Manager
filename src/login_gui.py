from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
import sql_handler as sql_handler



class LoginWidget(QWidget):

    def __init__(self, app):
        super().__init__()
        self.setFixedWidth(200)
        self.setFixedHeight(200)
        self.app = app
        self.host_entry = None
        self.username_entry = None
        self.password_entry = None
        self.port_entry = None
        self.main_layout = QVBoxLayout()
        self.build_login_widget()
        

    def build_login_widget(self):
        self.setLayout(self.main_layout)
        self.build_host_row()
        self.build_username_row()
        self.build_password_row()
        self.build_port_row()
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.main_layout.addWidget(self.login_button)
        self.setLayout(self.main_layout)


    def build_host_row(self):
        host_widget, host_layout = QWidget(), QHBoxLayout()
        host_label, host_entry = QLabel("Host: "), QLineEdit("localhost")
        host_layout.addWidget(host_label)
        host_layout.addWidget(host_entry)
        host_widget.setLayout(host_layout)
        self.main_layout.addWidget(host_widget)
        self.host_entry = host_entry

    def build_username_row(self):
        username_widget, username_layout = QWidget(), QHBoxLayout()
        username_label, username_entry = QLabel("Username: "), QLineEdit("postgres")
        username_layout.addWidget(username_label)
        username_layout.addWidget(username_entry)
        username_widget.setLayout(username_layout)
        self.main_layout.addWidget(username_widget)
        self.username_entry = username_entry

    def build_password_row(self):
        password_widget, password_layout = QWidget(), QHBoxLayout()
        password_label, password_entry = QLabel("Password: "), QLineEdit("admin")
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_entry)
        password_widget.setLayout(password_layout)
        self.main_layout.addWidget(password_widget)
        self.password_entry = password_entry


    def build_port_row(self):
        port_widget, port_layout = QWidget(), QHBoxLayout()
        port_label, port_entry = QLabel("Port: "), QLineEdit("5432")
        port_layout.addWidget(port_label)
        port_layout.addWidget(port_entry)
        port_widget.setLayout(port_layout)
        self.main_layout.addWidget(port_widget)
        self.port_entry = port_entry


    def login(self):
        params_db = {}
        params_db["host"] = self.host_entry.text()
        params_db["user"] = self.username_entry.text()
        params_db["password"] = self.password_entry.text()
        params_db["port"] = self.port_entry.text()
        self.try_to_log_in(params_db)
        
        

    def try_to_log_in(self, params):
        connection = sql_handler.DBManager.login_connect(params)
        if connection:
            self.accept_login_trial(params)
        else:
            self.deny_login_trial()

    def accept_login_trial(self, params):
        self.app.db_manager = sql_handler.DBManager(self.app, params)
        self.app.build_db_management_widget(self.username_entry.text())
        self.app.main_widget.setCurrentIndex(1)

    def deny_login_trial(self):
        self.app.raise_error(e="login_error", function=None, parameters=None, row_number=None, database_name=None)
