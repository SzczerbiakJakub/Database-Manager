from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
import table_manip
import table_query

class TableWidget(QWidget):

    def __init__(self, db_widget, queried):
        super().__init__()
        self.db_widget = db_widget
        self.app = db_widget.app
        self.queried = queried
        self.buttons = []
        self.layout = QVBoxLayout()
        self.create_ui()


    def create_ui(self):
        self.setLayout(self.layout)
        self.add_buttons()
        self.table = Table(self, self.queried)
        self.layout.addWidget(self.table)


    def add_buttons(self):
        add_row_button = QPushButton("Add row")
        add_row_button.clicked.connect(self.add_row)
        self.layout.addWidget(add_row_button)
        self.buttons.append(add_row_button)
        delete_row_button = QPushButton("Delete row")
        delete_row_button.clicked.connect(self.delete_row)
        self.layout.addWidget(delete_row_button)
        self.buttons.append(delete_row_button)
        add_column_button = QPushButton("Add column")
        add_column_button.clicked.connect(self.add_column)
        self.layout.addWidget(add_column_button)
        self.buttons.append(add_column_button)
        delete_column_button = QPushButton("Delete column")
        delete_column_button.clicked.connect(self.delete_column)
        self.layout.addWidget(delete_column_button)
        self.buttons.append(delete_column_button)
        query_button = QPushButton("Query table")
        query_button.clicked.connect(self.query_table)
        self.layout.addWidget(query_button)
        self.buttons.append(query_button)
        to_csv_button = QPushButton("Export table to csv...")
        to_csv_button.clicked.connect(self.export_table_to_csv)
        self.layout.addWidget(to_csv_button)
        self.buttons.append(to_csv_button)

    def export_table_to_csv(self):
        if self.queried:
            return self.db_widget.export_queried_table_to_csv()
        else:
            return self.db_widget.export_table_to_csv()

    def block_buttons(self):
        if self.db_widget.current_table is None:
            self.disable_buttons()
        else:
            self.enable_buttons()

    def disable_buttons(self):
        for button in self.buttons:
            button.setEnabled(False)

    def enable_buttons(self):
        for button in self.buttons:
            button.setEnabled(True)

    def add_row(self):
        return table_manip.CreateRowWindow(self.app)

    def delete_row(self):
        return table_manip.DeleteRowWindow(self.app)

    def add_column(self):
        return table_manip.CreateColumnWindow(self.app, self.queried)

    def delete_column(self):
        return table_manip.DeleteColumnWindow(self.app, self.queried)

    def query_table(self):
        query = table_query.CreateQueryWindow(self.app)



class Table(QTableWidget):

    def __init__(self, table_widget, queried):
        super().__init__()
        self.table_widget = table_widget
        self.queried = queried
        self.setFixedWidth(int(self.table_widget.app.screen_width/2))
        self.build_ui()


    def build_ui(self):
        app = self.table_widget.app
        if app.db_manager.current_initial_table is not None:
            if not self.queried:
                columns, rows, table_size = app.db_manager.get_table_content(current_database=self.table_widget.db_widget.current_database)
                if rows is not None:
                    self.setRowCount(table_size)
                    self.setColumnCount(len(columns))
                    self.setHorizontalHeaderLabels(columns)
                    for x in range(table_size):
                        for y in range(len(columns)):
                            item = QTableWidgetItem(str(rows[x][y]))
                            self.setItem(x, y, item)
            else:
                rows = app.db_manager.queried_table_rows
                if rows is not None:
                    self.setRowCount(app.db_manager.queried_table_rows_size)
                    self.setColumnCount(len(app.db_manager.queried_table_column_names))
                    self.setHorizontalHeaderLabels(app.db_manager.queried_table_column_names)
                    for x in range(app.db_manager.queried_table_rows_size):
                        for y in range(len(app.db_manager.queried_table_column_names)):
                            item = QTableWidgetItem(str(rows[x][y]))
                            self.setItem(x, y, item)
        self.verticalHeader().setVisible(False)


        