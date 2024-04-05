from PyQt5.QtWidgets import QFileDialog
import pandas as pd

def import_from_csv(create_table_window):
        filename, _ = QFileDialog.getOpenFileName(create_table_window, 'Open CSV File', '', 'CSV files (*.csv)')
        adjust_table_to_imported_csv(create_table_window, filename)
        return filename


def adjust_table_to_imported_csv(create_table_window, csv_filename):
        try:
            df = pd.read_csv(csv_filename, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(csv_filename, encoding="windows-1252")
        columns = df.columns.tolist()
        print(columns)
        first_row = df.values.tolist()[0]
        data_types = [df[column].dtype for column in columns]
        list_of_categories = tuple(zip(columns, data_types))
        create_table_window.create_ui(from_csv=True, categories=list_of_categories)


def get_dataframe(csv_filename):
    try:
        df = pd.read_csv(csv_filename, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(csv_filename, encoding="windows-1252")

    df = df.dropna()

    return df


def export_table_to_csv(rows, columns):
     df = pd.DataFrame(rows, columns=columns)
     save_to_csv(df)


def save_to_csv(dataframe):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_name, _ = QFileDialog.getSaveFileName(None, "Save CSV File", "", "CSV Files (*.csv)", options=options)
    file_name += ".csv"
    if file_name:
        dataframe.to_csv(file_name, index=False)
        print("CSV file saved successfully:", file_name)