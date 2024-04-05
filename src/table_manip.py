from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QComboBox, QHBoxLayout, QCheckBox
from comboboxes import LogicOperatorCombobox, TableColumnsCombobox, SignCombobox, DatatypeComboBox
from datatypes import DataTypes

class CreateRowWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.setWindowTitle("Insert new row")
        self.setGeometry(100, 100, 200, 100)
        self.inputs = {}
        self.create_ui()
        self.exec()

    def create_ui(self):
        vbox = QVBoxLayout()
        for column_name in self.app.db_manager.initial_table_column_names[1:]:
            hbox = QHBoxLayout()
            temp_widget = QWidget()
            label = QLabel(column_name)
            hbox.addWidget(label)
            input = QLineEdit()
            self.inputs[column_name] = input
            hbox.addWidget(input)
            temp_widget.setLayout(hbox)
            vbox.addWidget(temp_widget)
        button = QPushButton("Insert", self)
        button.setGeometry(100, 100, 100, 30)
        button.clicked.connect(self.close_dialog)
        vbox.addWidget(button)
        self.setLayout(vbox)
        

    def close_dialog(self):
        self.close()
        self.app.db_manager.create_new_row(self.inputs)
        self.app.main_widget.widget(1).rebuild_table_widget()
        db_tables_tree_widgets = self.app.main_widget.widget(1).db_tables_tree_widgets
        db_tables_tree_widgets.refresh_modified_table(self.app.db_manager.current_initial_table)


class DeleteRowWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.setWindowTitle("Delete row")
        self.setGeometry(100, 100, 200, 100)
        self.inputs = []
        self.layout = QVBoxLayout()
        self.create_ui()
        self.exec()

    def create_ui(self):
        self.setLayout(self.layout)
        self.build_options_widget()
        self.add_option_row()
        add_condition_button = QPushButton("Add condition", self)
        add_condition_button.setGeometry(100, 100, 100, 30)
        add_condition_button.clicked.connect(self.add_option_row)
        self.layout.addWidget(add_condition_button)
        button = QPushButton("Delete", self)
        button.setGeometry(100, 100, 100, 30)
        button.clicked.connect(self.close_dialog)
        self.layout.addWidget(button)
        
    def build_options_widget(self):
        self.options_widget = QWidget()
        self.options_widget_layout = QVBoxLayout()
        self.options_widget.setLayout(self.options_widget_layout)
        self.layout.addWidget(self.options_widget)


    def add_option_row(self):
        if len(self.inputs) > 0:
            option_row = DeleteRowOption(self, self.app, additional=True)
        else:
            option_row = DeleteRowOption(self, self.app)
        self.options_widget_layout.addWidget(option_row)
        self.inputs.append(option_row)

    def get_inputs(self):
        return [input.get_delete_condition() for input in self.inputs]

    def close_dialog(self):
        self.close()
        conditions = " ".join(self.get_inputs())
        self.app.db_manager.delete_row(conditions)
        self.app.main_widget.widget(1).rebuild_table_widget()
        db_tables_tree_widgets = self.app.main_widget.widget(1).db_tables_tree_widgets
        db_tables_tree_widgets.refresh_modified_table(self.app.db_manager.current_initial_table)


class DeleteRowOption(QWidget):

    def __init__(self, parent, app, additional=False):
        super().__init__()
        self.parent = parent
        self.app = app
        self.additional = additional
        self.layout = QHBoxLayout()
        self.and_or_box = None
        self.build_ui()
    
    def build_ui(self):
        self.setLayout(self.layout)
        delete_button = QPushButton("X")
        self.layout.addWidget(delete_button)
        delete_button.clicked.connect(self.delete_option)
        if self.additional:
            self.and_or_box = LogicOperatorCombobox()
            self.layout.addWidget(self.and_or_box)
        self.option_combobox = TableColumnsCombobox(self.app)
        self.layout.addWidget(self.option_combobox)
        self.sign_combobox = SignCombobox()
        self.layout.addWidget(self.sign_combobox)
        self.condition_input = QLineEdit()
        self.layout.addWidget(self.condition_input)


    def get_delete_condition(self):
        and_or_box_output = ""
        if self.and_or_box is not None:
            and_or_box_output = self.and_or_box.currentText()
        return f"{and_or_box_output} {self.option_combobox.currentText()} {self.sign_combobox.currentText()} {self.condition_input.text()}"
        
    def delete_option(self):
        self.parent.inputs.remove(self)
        self.deleteLater()
        



class CreateColumnWindow(QDialog):
    def __init__(self, parent, is_table_queried):
        super().__init__(parent)
        self.app = parent
        self.is_table_queried = is_table_queried
        self.setWindowTitle("Insert new column")
        self.setGeometry(100, 100, 200, 100)
        self.column_name = None
        self.data_inputs = {}
        self.default_variable = None
        self.constraints = {}
        self.create_ui()
        self.exec()

    def create_ui(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.create_name_widget())
        vbox.addWidget(self.create_data_type_widget())
        vbox.addWidget(self.create_variable_widget())
        vbox.addWidget(self.create_not_null_checkbox())
        vbox.addWidget(self.create_serial_checkbox())
        self.setLayout(vbox)
        
        button = QPushButton("Insert", self)
        button.setGeometry(100, 100, 100, 30)
        button.clicked.connect(self.close_dialog)
        vbox.addWidget(button)
        self.setLayout(vbox)
        
    def create_name_widget(self):
        name_widget, layout = QWidget(), QHBoxLayout()
        label, name_input = QLabel("New column: "), QLineEdit()
        layout.addWidget(label)
        self.column_name = name_input
        layout.addWidget(name_input)
        name_widget.setLayout(layout)
        return name_widget

    def create_data_type_widget(self):
        data_type_widget, layout = QWidget(), QHBoxLayout()
        data_type_variable_input = QLineEdit()
        data_type_input = DatatypeComboBox(data_type_variable_input)
        layout.addWidget(data_type_input)
        layout.addWidget(data_type_variable_input)
        self.data_inputs.update({"data type" : data_type_input})
        self.data_inputs.update({"data variable" : data_type_variable_input})
        data_type_widget.setLayout(layout)
        return data_type_widget

    def create_variable_widget(self):
        variable_widget, layout = QWidget(), QHBoxLayout()
        label, variable_input = QLabel("DEFAULT VAR:"), QLineEdit()
        layout.addWidget(label)
        layout.addWidget(variable_input)
        self.default_variable = variable_input
        variable_widget.setLayout(layout)
        return variable_widget

    def create_not_null_checkbox(self):
        not_null_checkbox = QCheckBox('NOT NULL', self)
        not_null_checkbox.setChecked(True)
        self.constraints.update({"not null" : not_null_checkbox})
        return not_null_checkbox
    
    def create_serial_checkbox(self):
        serial_checkbox = QCheckBox('SERIAL', self)
        serial_checkbox.setChecked(False)
        self.constraints.update({"serial" : serial_checkbox})
        return serial_checkbox

    def get_inputs(self):
        if self.data_inputs["data type"].data_variable_exists:
            data_type = self.data_inputs["data type"].currentText()
            data_var = self.data_inputs["data variable"].text()
            data_input = f"{data_type}({data_var})"
        else:
            data_input = self.data_inputs["data type"].currentText()

        var = self.default_variable.text()
        var = f"'{var}'" if self.data_inputs["data type"].currentText() in DataTypes.var_data_types else var

        inputs = {
                    "name" : self.column_name.text(),
                    "data" : data_input,
                    "variable" : var,
                    "not null" : "NOT NULL" if self.constraints["not null"].isChecked() else "",
                    "serial" : "SERIAL" if self.constraints["serial"].isChecked() else "",
                  }
        return inputs

    def close_dialog(self):
        self.close()
        inputs = self.get_inputs()
        self.app.db_manager.create_new_column(inputs, self.is_table_queried)
        self.app.main_widget.widget(1).rebuild_table_widget()
        db_tables_tree_widgets = self.app.main_widget.widget(1).db_tables_tree_widgets
        db_tables_tree_widgets.refresh_modified_table(self.app.db_manager.current_initial_table)


class DeleteColumnWindow(QDialog):
    def __init__(self, parent, is_table_queried):
        super().__init__(parent)
        self.app = parent
        self.is_table_queried = is_table_queried
        self.setWindowTitle("Delete table")
        self.setGeometry(100, 100, 200, 100)
        self.create_ui()
        self.exec()

    def create_ui(self):
        vbox = QVBoxLayout()
        self.input = QComboBox()
        columns, rows, size_of_table = self.app.db_manager.get_table_content()
        for column in columns:
            self.input.addItem(column)
        vbox.addWidget(self.input)
        button = QPushButton("Delete", self)
        button.setGeometry(100, 100, 100, 30)
        button.clicked.connect(self.close_dialog)
        vbox.addWidget(button)
        self.setLayout(vbox)
        

    def close_dialog(self):
        self.close()
        self.app.db_manager.delete_column(self.input.currentText(), self.is_table_queried)
        self.app.main_widget.widget(1).rebuild_table_widget()
        db_tables_tree_widgets = self.app.main_widget.widget(1).db_tables_tree_widgets
        db_tables_tree_widgets.refresh_modified_table(self.app.db_manager.current_initial_table)