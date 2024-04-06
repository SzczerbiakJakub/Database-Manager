from PyQt5.QtWidgets import QMessageBox, QPushButton



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
        self.exec_()

    def retry(self):
        self.app.retry(self.function, self.parameters)