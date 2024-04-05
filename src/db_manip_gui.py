from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QComboBox


class CreateDatabaseWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.setWindowTitle("Create new database")
        self.setGeometry(100, 100, 200, 100)
        self.create_ui()
        self.exec()


    def create_ui(self):
        vbox = QVBoxLayout()
        self.input = QLineEdit()
        vbox.addWidget(self.input)
        button = QPushButton("Create", self)
        button.setGeometry(100, 100, 100, 30)
        button.clicked.connect(self.close_dialog)
        vbox.addWidget(button)
        self.setLayout(vbox)
        

    def close_dialog(self):
        self.close()
        self.app.db_manager.create_new_database(self.input.text())


class DeleteDatabaseWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = parent
        self.setWindowTitle("Delete database")
        self.setGeometry(100, 100, 200, 100)
        self.create_ui()
        self.exec()


    def create_ui(self):
        vbox = QVBoxLayout()
        self.input = QComboBox()
        for x in self.app.db_manager.get_databases():
            self.input.addItem(x[0])
            #list_widget.setItemWidget(item, x_label)
        vbox.addWidget(self.input)
        button = QPushButton("Delete", self)
        button.setGeometry(100, 100, 100, 30)
        button.clicked.connect(self.close_dialog)
        vbox.addWidget(button)
        self.setLayout(vbox)
        

    def close_dialog(self):
        self.close()
        self.app.db_manager.delete_database(self.input.currentText())





