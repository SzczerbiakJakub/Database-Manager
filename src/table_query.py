from PyQt5.QtWidgets import QDialog, QLabel, QMessageBox, QVBoxLayout, QLineEdit, QWidget, QPushButton, QComboBox, QHBoxLayout, QCheckBox, QRadioButton
from comboboxes import DatatypeComboBox, LogicOperatorCombobox, SignCombobox, AgregateFunctionsCombobox



class CreateQueryWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.setWindowTitle("Query...")
        self.setGeometry(300, 100, 200, 100)
        self.condition = {"WHERE" : None, "GROUP BY" : None, "HAVING" : None}
        self.custom_column = False
        self.custom_column_input = QLineEdit()
        self.main_vbox = QVBoxLayout()
        self.setLayout(self.main_vbox)
        self.inputs = {}
        self.agregate_functions = {}
        self.list_of_selected = []
        self.selected_groupable = None
        self.query_condition_window = None
        self.create_ui()
        self.exec()
        


    def create_ui(self):
        for column_name in self.app.db_manager.initial_table_column_names:
            self.create_option(column_name)
        self.create_option("Custom", custom=True)
        join_button = QPushButton("Join", self)
        join_button.setGeometry(100, 100, 100, 30)
        join_button.clicked.connect(self.join_tables)
        self.main_vbox.addWidget(join_button)
        condition_button = QPushButton("Condition", self)
        condition_button.setGeometry(100, 100, 100, 30)
        condition_button.clicked.connect(self.set_condition)
        self.main_vbox.addWidget(condition_button)
        query_button = QPushButton("Query", self)
        query_button.setGeometry(100, 100, 100, 30)
        query_button.clicked.connect(self.close_dialog)
        self.main_vbox.addWidget(query_button)
        


    def create_menu_widget(self):
        #vbox = QVBoxLayout()
        ...
        #self.menu_widget.setLayout(self.main_vbox)
        #self.main_widget.addWidget(self.menu_widget)

    #def create_agregate_fu
        
    def get_selected_groupable(self, selected_columns):
        selected_groupable_list = []
        need_to_group_by = False
        for column in selected_columns:
            if column in self.agregate_functions.keys():
                if self.agregate_functions[column].currentText() == "-":
                    selected_groupable_list.append(column)
                else:
                    need_to_group_by = True
            else:
                selected_groupable_list.append(column)
        if len(selected_groupable_list) == 0 or not need_to_group_by:
            selected_groupable_list = None
            self.condition["GROUP BY"] = None
        else:
            self.condition["GROUP BY"] = ", ".join(selected_groupable_list)
        return selected_groupable_list
    
    def preprocess_selected_columns(self, list_of_columns):
        for i, item in enumerate(list_of_columns):
            if item in self.agregate_functions.keys():
                if self.agregate_functions[item].currentText() != "-":
                    preprocessed_item = self.preprocess_selected_column(item)
                    list_of_columns[i] = preprocessed_item
        return list_of_columns

    def preprocess_selected_column(self, column):
        if self.agregate_functions[column].currentText() != "-":
            preprocessed_item = self.agregate_functions[column].currentText()
            preprocessed_item += f"({column})"
        return preprocessed_item


    def create_option(self, column_name, custom=False):        
        hbox = QHBoxLayout()
        temp_widget = QWidget()
        radio_button_input = QRadioButton()
        hbox.addWidget(radio_button_input)
        label = QLabel(column_name)
        hbox.addWidget(label)
        if custom:
            self.custom_column = True
            hbox.addWidget(self.custom_column_input)
            radio_button_input.clicked.connect(self.toggle_custom_input)
            self.custom_column_input.setEnabled(False)
        else:
            agregate_function_combobox = self.create_agregate_function_combobox()
            hbox.addWidget(agregate_function_combobox)
            self.inputs.update({column_name : radio_button_input})
            self.agregate_functions.update({column_name : agregate_function_combobox})
        temp_widget.setLayout(hbox)
        self.main_vbox.addWidget(temp_widget)
        
    def create_agregate_function_combobox(self):
        agregate_function_combobox = AgregateFunctionsCombobox()
        #sign_combobox.addItem("!=")
        return agregate_function_combobox
    
    def toggle_custom_input(self):
        sender = self.sender()
        if sender.isChecked():
            self.custom_column_input.setEnabled(True)
        else:
            self.custom_column_input.setEnabled(False)
            self.custom_column_input.setText("")

    def set_condition(self, auto_apply=False):
        self.list_of_selected = self.get_selected_columns()
        print(self.list_of_selected)
        if len(self.list_of_selected) == 0:
            self.show_no_columns_error()
        else:
            self.query_condition_window = QueryConditionWindow(self, self.get_condition_column_options(), self.list_of_selected, auto_apply=auto_apply)

    def join_tables(self):
        ...

    def get_raw_selected_columns(self):
        raw_selected_columns = [column for column in self.inputs.keys() if self.inputs[column].isChecked()]
        if len(self.custom_column_input.text()) > 0:
            custom_input = self.custom_column_input.text().replace(",", " ")
            raw_selected_columns.extend(custom_input.split())
        return raw_selected_columns

    def get_selected_columns(self):
        selected_columns = self.get_raw_selected_columns()
        selected_columns = self.preprocess_selected_columns(selected_columns)
        print(selected_columns)
        return selected_columns
    """def define_group_by(self):
        list_of_selected = [x for x in self.inputs.keys() if self.inputs[x].isChecked()]
        if len(list_of_selected) == 0:
            self.show_no_columns_error()
        else:
            query_group_by_window = QueryGroupByWindow(self, list_of_selected)"""
    
    def get_condition_column_options(self):
        options = self.app.db_manager.initial_table_column_names
        options.extend([option for option in self.get_selected_columns() if option not in self.app.db_manager.initial_table_column_names])
        return options

    def close_dialog(self):
        self.close()
        #print(self.condition)
        #print(self.inputs)
        self.selected_groupable = self.get_selected_groupable(self.get_raw_selected_columns())
        #queried_columns = [column for column in self.inputs.keys() if self.inputs[column].isChecked()]
        queried_columns = self.get_selected_columns()
        """if self.custom_column:
            custom_select = self.custom_column_input.text()
        else:
            custom_select = None"""
        #self.app.db_manager.slice_current_table(queried_columns, self.condition, custom_select=custom_select)
        """if self.query_condition_window is not None:
            queried_columns = [name for name in self.query_condition_window.selected_names
                           if self.query_condition_window.selected_names[name] in self.list_of_selected]"""
        print(queried_columns)
        print(self.selected_groupable)
        self.app.db_manager.slice_current_table(queried_columns, self.condition)
        #self.app.main_widget.widget(2).rebuild_table_widget()


    def show_no_columns_error(self):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText("No columns selected. Select which columns to query before aplying condition.")
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()


class QueryConditionWindow(QDialog):

    def __init__(self, query_window, all_columns, selected_columns, auto_apply):
        super().__init__()
        self.query_window = query_window
        #self.selected_columns = all_columns
        self.setWindowTitle("Insert condition")
        self.setGeometry(200, 200, 300, 200)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.condition_options_list = []
        self.selected_list = {}
        self.keyword_condition_dict = self.get_keyword_condition_dict(all_columns)
        #self.selected_preprocessed_list = {}
        self.selected_columns = selected_columns
        #self.condition = None
        self.create_ui()
        self.exec()
        if auto_apply:
            self.apply_condition()

    def create_ui(self):
        self.conditions_layout = self.create_conditions_layout()
        self.create_condition_option()
        add_condition_button = QPushButton("Add condition", self)
        add_condition_button.setGeometry(100, 100, 100, 30)
        add_condition_button.clicked.connect(self.add_condition)
        self.main_layout.addWidget(add_condition_button)
        apply_button = QPushButton("Apply", self)
        apply_button.setGeometry(100, 100, 100, 30)
        apply_button.clicked.connect(self.apply_condition)
        self.main_layout.addWidget(apply_button)

    def create_condition_option(self, additional=False):
        condition_option_row = ConditionOptionRow(self, additional)
        self.condition_options_list.append(condition_option_row)
        #self.main_layout.addWidget(option_widget)
        self.conditions_layout.addWidget(condition_option_row)

    def create_conditions_layout(self):
        condition_widget = QWidget()
        condidions_layout = QVBoxLayout()
        condition_widget.setLayout(condidions_layout)
        self.main_layout.addWidget(condition_widget)
        return condidions_layout
    
    def update_keyword_dict(self, keyword_dict):
        key_list = list(keyword_dict.keys())
        updated_keyword_dict = {}
        for key in key_list:
            if key in self.query_window.agregate_functions.keys():
                if self.query_window.agregate_functions[key].currentText() != "-":
                    keyword_dict.pop(key)
                    preprocessed_key = self.query_window.preprocess_selected_column(key)
                    updated_keyword_dict.update({preprocessed_key : "HAVING"})
            else:
                for function_keyword in AgregateFunctionsCombobox.functions:
                    if function_keyword in key:
                        updated_keyword_dict.update({key : "HAVING"})
            
        keyword_dict.update(updated_keyword_dict)
        
    def get_keyword_condition_dict(self, all_columns):
        keyword_condition_dict = {}
        for column in all_columns:
            keyword_condition_dict.update({column : "WHERE"})
        self.update_keyword_dict(keyword_condition_dict)
        return keyword_condition_dict

    def add_condition(self):
        if len(self.condition_options_list) == 0:
            self.create_condition_option()
        else:
            self.create_condition_option(additional=True)
        
    def apply_condition(self):
        where_condition = ""
        having_condition = ""
        for option in self.condition_options_list:
            returned_condition = option.return_condition()
            print(returned_condition)
            if self.keyword_condition_dict[returned_condition[1]] == "WHERE":
                if where_condition != "":
                    where_condition += returned_condition[2]
                    where_condition += " "
                where_condition += returned_condition[0]
            elif self.keyword_condition_dict[returned_condition[1]] == "HAVING":
                #group_query = True
                if having_condition != "":
                    having_condition += returned_condition[2]
                    having_condition += " "
                having_condition += returned_condition[0]
        #print(condition)
        if where_condition != "":
            self.query_window.condition["WHERE"] = where_condition
        #if group_by_condition != "":
        #if group_query:
        self.query_window.condition["GROUP BY"] = self.return_group_by()
        if having_condition != "":
            self.query_window.condition["HAVING"] = having_condition

        x = self.query_window.condition["WHERE"]
        y = self.query_window.condition["GROUP BY"]
        z = self.query_window.condition["HAVING"]
        print(f"WHERE {x} GROUP BY {y} HAVING {z}")
        self.close_dialog()

    def return_group_by(self):
        where_list = ""
        having_list = ""
        for column in self.selected_columns:
            if self.keyword_condition_dict[column] == "WHERE" and column in self.query_window.list_of_selected:
                if where_list != "":
                    where_list += ", "
                where_list += column
            elif self.keyword_condition_dict[column] == "HAVING":
                if having_list != "":
                    having_list += ", "
                having_list += column
        if having_list == "" or where_list == "":
            where_list = None
            
        return where_list

    def close_dialog(self):
        self.close()

    



class ConditionOptionRow(QWidget):

    def __init__(self, condition_window, additional):
        super().__init__()
        self.condition_window = condition_window
        self.additional = additional
        self.layout = QHBoxLayout()
        self.and_or_box = None
        self.condition_input = None
        self.setLayout(self.layout)
        self.create_condition_option()

    def create_condition_option(self):
        self.delete_button = QPushButton("X", self)
        self.delete_button.setGeometry(100, 100, 100, 30)
        self.delete_button.clicked.connect(self.delete_row)
        self.layout.addWidget(self.delete_button)
        if self.additional:
            """self.and_or_box = QComboBox()
            self.and_or_box.setFixedWidth(50)
            self.and_or_box.addItem("AND")
            self.and_or_box.addItem("OR")
            self.layout.addWidget(self.and_or_box)"""
            self.and_or_box = LogicOperatorCombobox()
            self.layout.addWidget(self.and_or_box)
        self.columns = QComboBox()
        self.columns.setFixedWidth(150)
        for item in self.condition_window.keyword_condition_dict.keys():
            self.columns.addItem(item)
        self.layout.addWidget(self.columns)
        self.sign_combobox = self.create_sign_combobox()
        self.condition_input = QLineEdit()
        self.condition_input.setFixedWidth(150)
        self.layout.addWidget(self.condition_input)

    def create_sign_combobox(self):
        """sign_combobox = QComboBox()
        sign_combobox.setFixedWidth(50)
        sign_combobox.addItem("<")
        sign_combobox.addItem("<=")
        sign_combobox.addItem("=")
        sign_combobox.addItem(">=")
        sign_combobox.addItem(">")
        sign_combobox.addItem("!=")"""
        sign_combobox = SignCombobox()
        self.layout.addWidget(sign_combobox)
        return sign_combobox

    def delete_row(self):
        if self == self.condition_window.condition_options_list[0]:
            if len(self.condition_window.condition_options_list) > 1:
                second_option = self.condition_window.condition_options_list[1]
                if second_option.and_or_box is not None:
                    second_option.layout.removeWidget(second_option.and_or_box)
                    second_option.and_or_box = None
        self.condition_window.condition_options_list.remove(self)
        self.condition_window.conditions_layout.removeWidget(self)

    def return_condition(self):
        if self.condition_input.text() == "":
            condition = ""
            and_or_prefix = ""
        else:
            if self.and_or_box is not None:
                and_or_prefix = self.and_or_box.currentText()
            else:
                and_or_prefix = ""
            condition = self.columns.currentText()
            condition += " "
            condition += self.sign_combobox.currentText()
            condition += " "
            condition += self.condition_input.text()
            condition += " "

        return (condition, self.columns.currentText(), and_or_prefix)