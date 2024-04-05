from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QLabel
import table_gui as table
import dbs_tables_gui as dbs_tables
import db_manip_gui as db_manip
import table_creator_gui as table_creator
import csv_manip


class DbManagementWidget(QWidget):

    def __init__(self, app, username):
        super().__init__()
        self.app = app
        self.username = username
        self.current_database = None
        self.current_table = None
        self.curent_row = None
        self.database_buttons = []
        self.table_buttons = []
        self.main_layout = QHBoxLayout()
        self.build_ui()
        
    def build_ui(self):
        
        self.build_db_tables_widget()
        self.disable_table_buttons()
        self.build_table_widget()
        self.table_widget.disable_buttons()
        self.setLayout(self.main_layout)

    def build_table_widget(self, queried=False):
        self.table_widget = table.TableWidget(self, queried=queried)
        self.main_layout.addWidget(self.table_widget)

    def rebuild_table_widget(self, queried=False):
        self.main_layout.removeWidget(self.table_widget)
        self.build_table_widget(queried)

    def build_user_panel_widget(self):
        self.user_panel_widget = UserPanelWidget(self)

    def rebuild_user_panel_widget(self):
        self.main_layout.removeWidget(self.user_panel_widget)
        self.build_user_panel_widget()


    def build_db_tables_widget(self):
        self.db_tables_widget = QWidget()
        vbox = QVBoxLayout()
        self.build_user_panel_widget()
        vbox.addWidget(self.user_panel_widget)
        create_database_button = QPushButton("Create database")
        create_database_button.clicked.connect(self.add_database)
        self.database_buttons.append(create_database_button)
        vbox.addWidget(create_database_button)
        delete_database_button = QPushButton("Delete database")
        delete_database_button.clicked.connect(self.delete_database)
        self.database_buttons.append(delete_database_button)
        vbox.addWidget(delete_database_button)
        create_table_button = QPushButton("Create table")
        create_table_button.clicked.connect(self.add_table)
        self.table_buttons.append(create_table_button)
        vbox.addWidget(create_table_button)
        delete_table_button = QPushButton("Delete table")
        delete_table_button.clicked.connect(self.delete_table)
        self.table_buttons.append(delete_table_button)
        vbox.addWidget(delete_table_button)

        self.db_tables_tree_widgets = dbs_tables.DatabaseTablesWidget(self, self.app)
        vbox.addWidget(self.db_tables_tree_widgets)
        self.db_tables_widget.setLayout(vbox)
        self.db_tables_widget.setFixedWidth(400)
        self.main_layout.addWidget(self.db_tables_widget)

    def rebuild_db_tables_widget(self):
        self.db_tables_tree_widgets.refresh()
        self.render()

    def home(self):
        self.app.build_home_widget()

    def database_selected(self, item):
        self.app.db_manager.current_database = item.text()
        tables = self.app.db_manager.get_database_tables()
        self.current_database = item.text()
        self.render()
        self.rebuild_dbs_tables()

    def table_selected(self, item):
        self.app.db_manager.current_initial_table = item.text()
        columns, rows, number_of_rows = self.app.db_manager.get_table_content()
        self.app.main_widget.widget(2).rebuild_table_widget()
        self.render()

    def add_database(self):
        database_window = db_manip.CreateDatabaseWindow(self.app)
        self.rebuild_db_tables_widget()
    
    def delete_database(self):
        database_window = db_manip.DeleteDatabaseWindow(self.app)
        self.rebuild_db_tables_widget()

    def add_table(self):
        if self.app.db_manager.current_database is not None:
            table_window = table_creator.CreateTableWindow(self.app)
        else:
            print("No database selected")
    
    def delete_table(self):
        return table_creator.DeleteTableWindow(self.app)

    def disable_table_buttons(self):
        for button in self.table_buttons:
            button.setEnabled(False)

    def enable_table_buttons(self):
        for button in self.table_buttons:
            button.setEnabled(True)

    def render(self):
        self.user_panel_widget.refresh()
        self.table_widget.block_buttons()
        if self.current_database is None:
            self.disable_table_buttons()
        else:
            self.enable_table_buttons()


    def export_table_to_csv(self):
        rows = self.app.db_manager.initial_table_rows
        columns = self.app.db_manager.initial_table_column_names
        csv_manip.export_table_to_csv(rows, columns)


    def export_queried_table_to_csv(self):
        rows = self.app.db_manager.queried_table_rows
        columns = self.app.db_manager.queried_table_column_names
        csv_manip.export_table_to_csv(rows, columns)



class UserPanelWidget(QWidget):

    def __init__(self, db_management_widget):
        super().__init__()
        self.db_management_widget = db_management_widget
        self.greeting_label = None
        self.current_database_label = None
        self.current_table_label = None
        self.layout = QVBoxLayout()
        self.build_ui()

    def build_ui(self):
        self.setLayout(self.layout)
        self.greeting_label = QLabel(f"Hello, {self.db_management_widget.username}")
        self.layout.addWidget(self.greeting_label)
        self.current_database_label = QLabel()
        self.layout.addWidget(self.current_database_label)
        self.current_table_label = QLabel()
        self.layout.addWidget(self.current_table_label)
        self.log_out_button = QPushButton("LOG OUT")
        self.log_out_button.clicked.connect(self.disconnect)
        self.layout.addWidget(self.log_out_button)
        self.refresh()
    
    def get_current_database(self):
        current_database = self.db_management_widget.current_database
        return "-" if current_database is None else current_database

    def get_current_table(self):
        current_table = self.db_management_widget.current_table
        return "-" if current_table is None else current_table
    
    def refresh(self):
        self.current_database_label.setText(f"Current database: {self.get_current_database()}")
        self.current_table_label.setText(f"Current table: {self.get_current_table()}")

    def disconnect(self):
        self.db_management_widget.app.main_widget.setCurrentIndex(0)
        self.db_management_widget.app.destroy_db_management_widget()