from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class DatabaseTablesWidget(QTreeWidget):

    def __init__(self, db_management_widget, app):
        super().__init__()
        self.db_management_widget = db_management_widget
        self.app = app
        self.available_databases = {}
        self.database_tables = {}
        self.tables_items_dict = {}
        self.build_available_dbs_widget()
        self.build_dbs_tables()
        self.expandAll()
        self.itemClicked.connect(self.handleItemClick)

    def build_available_dbs_widget(self):
        self.setHeaderLabels(['Databases'])
        for x in self.app.db_manager.get_databases():
            database = QTreeWidgetDatabaseItem(self, [x[0]])
            self.available_databases.update({x[0] : database})

    def rebuild_available_dbs_widget(self):
        self.main_layout.removeWidget(self.available_dbs_widget)
        self.build_available_dbs_widget()

    def build_dbs_tables(self):
        for x in self.available_databases.keys():
            self.app.db_manager.current_database = x
            tables = self.app.db_manager.get_database_tables()
            list_of_tables = []
            for y in tables:
                y_size = self.app.db_manager.get_table_size(y)
                table = QTreeWidgetTableItem(self.app, self.available_databases[x], str(y))
                self.tables_items_dict.update({str(y): table})
                self.database_tables.update({str(y) : x})

    def rebuild_dbs_tables(self):
        self.main_layout.removeWidget(self.dbs_tables_widget)
        self.build_dbs_tables()

    def handleItemClick(self, item, column):
        if isinstance(item, QTreeWidgetTableItem):
            self.app.db_manager.current_database = self.database_tables[item.name]
            self.app.db_manager.current_initial_table = item.name
            columns, rows, number_of_rows = self.app.db_manager.get_table_content()
            self.db_management_widget.rebuild_table_widget()
            self.db_management_widget.current_database = self.database_tables[item.name]
            self.db_management_widget.current_table = item.name
            self.db_management_widget.render()
        elif isinstance(item, QTreeWidgetDatabaseItem):
            self.app.db_manager.current_database = item.text(0)
            self.db_management_widget.current_database = item.text(0)
            self.db_management_widget.render()


    def database_selected(self, item):
        self.app.db_manager.current_database = item.text()
        tables = self.app.db_manager.get_database_tables()

    def table_selected(self, item):
        self.app.db_manager.current_initial_table = item.text()
        columns, rows, number_of_rows = self.app.db_manager.get_table_content()
        self.db_management_widget.rebuild_table_widget()
        self.rebuild_table_widget()

    def refresh(self):
        self.clear()
        self.available_databases = {}
        self.database_tables = {}
        self.build_available_dbs_widget()
        self.build_dbs_tables()
        self.expandAll()

    def refresh_modified_table(self, table_name):
        self.tables_items_dict[table_name].refresh()



class QTreeWidgetDatabaseItem(QTreeWidgetItem):

    def __init__(self, tree_widget, item):
        super().__init__(tree_widget, item)


class QTreeWidgetTableItem(QTreeWidgetItem):

    def __init__(self, app, tree_widget, name):
        super().__init__(tree_widget, [""])
        self.app = app
        self.name = name
        self.size = self.get_table_size()
        self.rename()
        
    def rename(self):
        self.setText(0, f"{self.name} ({self.size})")

    def get_table_size(self):
        return self.app.db_manager.get_table_size(self.name)

    def refresh(self):
        self.size = self.get_table_size()
        self.rename()
