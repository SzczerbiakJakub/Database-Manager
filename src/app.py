from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QMainWindow, QHBoxLayout, QWidget, QPushButton, QStackedWidget
import login_gui as login
import db_manager_gui as db_manager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DB Manager")
        self.screen_width, self.screen_size = self.get_screen_size()
        self.setGeometry(0, 0, self.screen_width, self.screen_size)
        self.db_manager = None
        self.home_widget = None
        self.db_management_widget = None
        self.login_widget = None
        self.main_widget = QStackedWidget()
        self.build_app()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setCurrentIndex(0)


    def build_app(self):
        self.build_home_widget()
        
    def build_home_widget(self):
        self.home_widget = HomeWidget(self)
        self.main_widget.addWidget(self.home_widget)

    def build_db_management_widget(self, username):
        self.db_management_widget = db_manager.DbManagementWidget(self, username)
        self.main_widget.addWidget(self.db_management_widget)

    def destroy_db_management_widget(self):
        self.db_management_widget = None
        self.main_widget.removeWidget(self.db_management_widget)

    def get_screen_size(self):
        desktop = QDesktopWidget()
        screen_geometry = desktop.screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        return screen_width, screen_height

    def raise_error(self, e, function=None, parameters=None, row_number=None, database_name=None):
        self.error_box = ErrorBox(self, e, function, parameters, row_number, database_name)
        
            
    def retry(self, function, parameters):
        function(parameters[0], parameters[1], parameters[2])


class ErrorBox(QMessageBox):

    def __init__(self, app, e, function, parameters, row_number, database_name):
        super().__init__()
        self.app = app
        self.function = function
        self.parameters = parameters
        self.setIcon(QMessageBox.Critical)
        self.setWindowTitle("Error")
        if e == "login_error":
            self.setText(f"Acces denied: invalid login data")
        
        elif e.pgcode == '23502':  # '23502' is the error code for NotNullViolation
            if row_number is None:
                row_number = "UNK"
            self.setText(f"NotNullViolation: Attempted to insert NULL value into a column with NOT NULL constraint. Null-valued row no.: {row_number}")
        elif e.pgcode == '55006':  # '55006' is the error code for ObjectInUse
            if database_name is None:
                database_name = "UNK"
            self.setText(f"The database {database_name} is currently in use or locked by another process.")
        else:
            self.setText(f"An error occurred: {e}")
        self.setStandardButtons(QMessageBox.Ok)
        retry_button = QPushButton("Retry")
        retry_button.clicked.connect(self.retry)
        self.addButton(retry_button, QMessageBox.ActionRole)
        result = self.exec_()

    def retry(self):
        self.app.retry(self.function, self.parameters)


class HomeWidget(QWidget):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.main_layout = QHBoxLayout()
        self.build_ui()


    def build_ui(self):
        self.setLayout(self.main_layout)
        self.login_widget = login.LoginWidget(self.app)
        self.main_layout.addWidget(self.login_widget)