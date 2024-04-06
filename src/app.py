from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QStackedWidget
import home_widget_gui as home
import db_manager_gui as db_manager
from error_handler import ErrorBox


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("DB Manager")
        self.screen_width, self.screen_height = self.get_screen_size()
        #self.setGeometry(0, 0, self.screen_width, self.screen_height)
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
        self.home_widget = home.HomeWidget(self)
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





