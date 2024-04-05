from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QWidget, QPushButton, QComboBox, QHBoxLayout, QCheckBox, QRadioButton
from comboboxes import DatatypeComboBox
import csv_manip



class CreateTableWindow(QDialog):

    """data_types = {'INTEGER', 'SMALLINT', 'BIGINT', 'DECIMAL', 'FLOAT',
                    'CHAR', 'VARCHAR', 'TEXT', 'TIME', 'DATE', 'TIMESTAMP',
                    'INTERVAL', 'BOOLEAN', 'BINARY', 'VARBINARY', 'BYTEA',
                    'ARRAY', 'JSON', 'UUID', 'XML', 'GEOMETRY'}
    
    var_data_types = {'CHAR', 'VARCHAR', 'BINARY', 'VARBINARY'}"""

    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.rows = []
        self.row_inputs = []
        self.from_csv = False
        self.csv_filename = None
        self.primary_key_selected = None
        self.setWindowTitle("Create new table")
        self.setGeometry(100, 100, 200, 100)
        self.vbox = QVBoxLayout()
        self.create_ui()
        self.setLayout(self.vbox)
        self.exec()


    def create_ui(self, from_csv=False, categories=None):
        if from_csv:
            self.clear_layout()
            self.from_csv = True
        self.table_name = QLineEdit()
        self.vbox.addWidget(self.table_name)
        self.options_widget = QWidget()
        self.options_vbox = QVBoxLayout()
        self.options_widget.setLayout(self.options_vbox)
        if from_csv and categories is not None:
            for item in categories:
                self.create_category_option_row(category=item)
        else:
            self.create_option_row()
        self.vbox.addWidget(self.options_widget)

        add_option_button = QPushButton("Add option", self)
        add_option_button.clicked.connect(self.create_option_row)
        self.vbox.addWidget(add_option_button)

        from_csv_button = QPushButton("Import from CSV file", self)
        from_csv_button.clicked.connect(self.import_table_from_csv)
        self.vbox.addWidget(from_csv_button)

        create_table_button = QPushButton("Create", self)
        create_table_button.clicked.connect(self.close_dialog)
        self.vbox.addWidget(create_table_button)


    def clear_layout(self):
        for i in reversed(range(self.vbox.count())):
            widget = self.vbox.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.rows.clear()
        self.row_inputs.clear()


    def create_option_row(self):
        row = CreateTableOptionRow(self, category=None)
        self.options_vbox.addWidget(row)
        self.rows.append(row)
        self.row_inputs.append(row.row_inputs)

    def create_category_option_row(self, category):
        row = CreateTableOptionRow(self, category)
        self.options_vbox.addWidget(row)
        self.rows.append(row)
        self.row_inputs.append(row.row_inputs)

    def close_dialog(self):
        self.close()
        current_database = self.app.main_widget.widget(1).current_database
        option_list, options_data_types = self.get_row_values()
        table_name = self.table_name.text()
        self.app.db_manager.create_new_table(table_name, option_list, current_database=current_database)
        self.app.main_widget.widget(1).rebuild_db_tables_widget()
        #if self.csv_filename is not None:
        if self.from_csv:
            column_names = tuple(zip([x[0] for x in option_list], options_data_types))
            self.app.db_manager.create_new_rows_from_csv(table_name, column_names, self.csv_filename, current_database=current_database)
            self.app.main_widget.widget(1).rebuild_table_widget()
            self.csv_filename = None

            
    def format_column_names(self, name):
        name = name.replace(" ", "_")
        name = name.replace("-", "")
        name = name.replace("+", "")
        name = name.replace("/", "")
        name = name.replace("'", "")
        name = name.replace('"', '')
        name = name.replace(";", "")
        name = name.replace("(", "")
        name = name.replace(")", "")
        return name

    def get_row_values(self):
        inputs = []
        data_types = []
        for x in self.row_inputs:
            values = []

            values.append(self.format_column_names(x['name'].text()))
            
            if x['serial'].isChecked():
                values.append('SERIAL')
            else:
                if x['data variable'].isEnabled():
                    command = x['data type'].currentText() + "(" + x['data variable'].text() +")"
                    values.append(command)
                else:
                    values.append(x['data type'].currentText())
                data_types.append(x['data type'].currentText())
                if x['not null'].isChecked():
                    values.append('NOT NULL')
                else:
                    values.append('NULL')
            if x['primary key'].isChecked():
                values.append('PRIMARY KEY')
            else:
                values.append('')
            inputs.append(values)
        return inputs, data_types

    def import_table_from_csv(self):
        self.csv_filename = csv_manip.import_from_csv(self)

    


class CreateTableOptionRow(QWidget):

    def __init__(self, parent_window, category=None):
        super().__init__()
        self.parent_window = parent_window
        self.row_inputs = self.build(category)


    def build(self, category):
        row_inputs = {}
        hbox = QHBoxLayout()
        #   DELETE ROW
        delete_row_button = QPushButton("X")
        delete_row_button.clicked.connect(self.delete_row)
        hbox.addWidget(delete_row_button)
        #   NAME INPUT
        name_input = QLineEdit()
        if category is not None:
            name_input.setText(category[0])
        hbox.addWidget(name_input)
        row_inputs.update({"name" : name_input})
        #   LINE EDIT INPUT
        data_type_variable_input = QLineEdit()
        #   DATA TYPE INPUT
        data_type_input = DatatypeComboBox(data_type_variable_input)#QComboBox()
        #self.add_options_to_combobox(data_type_input)
        if category is not None:
            data_type_input.set_datatype_from_category(category[1])
        #data_type_input.currentIndexChanged.connect(data_type_input.toggle_line_edit)
        hbox.addWidget(data_type_input)
        #data_type_input.toggle_line_edit()
        row_inputs.update({"data type" : data_type_input})
        #row_inputs.append(data_type_input)
        hbox.addWidget(data_type_variable_input)
        row_inputs.update({"data variable" : data_type_variable_input})
        #   NOT NULL INPUT
        not_null_checkbox = QCheckBox('NOT NULL', self)
        not_null_checkbox.setChecked(True)
        hbox.addWidget(not_null_checkbox)
        row_inputs.update({"not null" : not_null_checkbox})
        #row_inputs.append(not_null_checkbox)
        #   SERIAL INPUT
        serial_checkbox = QCheckBox('SERIAL', self)
        serial_checkbox.setChecked(False)
        hbox.addWidget(serial_checkbox)
        row_inputs.update({"serial" : serial_checkbox})
        #row_inputs.append(serial_checkbox)
        #   PRIMARY KEY INPUT
        primary_key_radiobutton = QRadioButton('PRIMARY KEY', self)
        primary_key_radiobutton.clicked.connect(self.set_primary_key)
        hbox.addWidget(primary_key_radiobutton)
        row_inputs.update({"primary key" : primary_key_radiobutton})
        self.setLayout(hbox)
        return row_inputs

    def set_primary_key(self):
        sender = self.sender()
        if self.parent_window.primary_key_selected is None:
            self.parent_window.primary_key_selected = sender
        else:
            self.parent_window.primary_key_selected.setChecked(False)
            self.parent_window.primary_key_selected = sender

    def add_options_to_combobox(self, combobox):
        for item in CreateTableWindow.data_types:
            combobox.addItem(item)

    def delete_row(self):
        self.deleteLater()



class DeleteTableWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.setWindowTitle("Delete table")
        self.setGeometry(100, 100, 200, 100)
        self.create_ui()
        self.exec()

    def create_ui(self):
        vbox = QVBoxLayout()
        self.input = QComboBox()
        self.app.db_manager.get_database_tables(self.app.main_widget.widget(1).current_database)
        #print(self.app.db_manager.table_names)
        for x in self.app.db_manager.table_names:
            self.input.addItem(x)
            #list_widget.setItemWidget(item, x_label)
        vbox.addWidget(self.input)
        button = QPushButton("Delete", self)
        button.setGeometry(100, 100, 100, 30)
        button.clicked.connect(self.close_dialog)
        vbox.addWidget(button)
        self.setLayout(vbox)
        

    def close_dialog(self):
        self.close()
        self.app.db_manager.delete_table(self.input.currentText(), self.app.main_widget.widget(1).current_database)