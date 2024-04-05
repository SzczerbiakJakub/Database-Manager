from PyQt5.QtWidgets import QComboBox
from datatypes import DataTypes

class DatatypeComboBox(QComboBox):

    def __init__(self, datatype_line_edit, data_types=DataTypes.data_types, var_data_types=DataTypes.var_data_types):
        super().__init__()
        self.datatype_line_edit = datatype_line_edit
        self.data_types = data_types
        self.var_data_types = var_data_types
        self.currentIndexChanged.connect(self.toggle_line_edit)
        self.data_variable_exists = False
        self.add_options()
        self.toggle_line_edit()

    def toggle_line_edit(self):
        selected_data_type = self.currentText()
        if selected_data_type in self.var_data_types:
            self.unblock_data_variable_input()
        else:
            self.block_data_variable_input()

    def unblock_data_variable_input(self):
        self.datatype_line_edit.setEnabled(True)
        self.data_variable_exists = True
        self.datatype_line_edit.setText('255')

    def block_data_variable_input(self):
        self.datatype_line_edit.setEnabled(False)
        self.data_variable_exists = False
        self.datatype_line_edit.setText('')

    def set_datatype_from_category(self, category_data_type):
        if ("int" in str(category_data_type)):
            self.setCurrentText("INTEGER")
        elif ("float" in str(category_data_type)):
            self.setCurrentText("FLOAT")
        elif (category_data_type == "O"):
            self.setCurrentText("VARCHAR")

    def add_options(self):
        for item in self.data_types:
            self.addItem(item)


class TableColumnsCombobox(QComboBox):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.add_options()

    def add_options(self):
        for column in self.app.db_manager.initial_table_column_names:
            self.addItem(column)



class LogicOperatorCombobox(QComboBox):

    operations = ["AND", "OR"]

    def __init__(self):
        super().__init__()
        self.setFixedWidth(50)
        self.add_options()

    def add_options(self):
        for operation in LogicOperatorCombobox.operations:
            self.addItem(operation)


class SignCombobox(QComboBox):

    signs = ['<', '<=', '=', '>=', '>', '!=']

    def __init__(self):
        super().__init__()
        self.setFixedWidth(50)
        self.add_options()

    def add_options(self):
        for sign in SignCombobox.signs:
            self.addItem(sign)

class AgregateFunctionsCombobox(QComboBox):

    functions = {"-", "COUNT", "SUM", "AVG", "MAX", "MIN"}

    def __init__(self):
        super().__init__()
        self.setFixedWidth(100)
        self.add_options()

    def add_options(self):
        for function in AgregateFunctionsCombobox.functions:
            self.addItem(function)
        self.setCurrentText("-")