import psycopg2
from psycopg2 import Error
import time
import csv_manip
import re
    


class DBManager:

    syntax_valid_characters = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz_0123456789"

    def __init__(self, app, params):
        self.app = app
        self.params = params
        self.current_database = None
        self.table_names = None
        self.current_initial_table = None
        self.initial_table_column_names = None
        self.initial_table_rows_size = 0
        self.initial_table_rows = None

        self.queried_list_of_columns = None
        self.queried_table_column_names = None
        self.queried_table_rows_size = 0
        self.queried_table_rows = None


    def connect(self, dbname=None):
        params = self.params
        if dbname is None:
            if self.current_database is not None:
                params["dbname"] = self.current_database
        else:
            params["dbname"] = dbname
        try:
            connection = psycopg2.connect(**params)
        except(Exception, psycopg2.DatabaseError) as error:
            ...
            
        cur = connection.cursor()
        cur.execute("SELECT version()")
        db_version = cur.fetchone()
        connection.commit()
        return connection
    

    @staticmethod
    def login_connect(params):
        connected = False
        try:
            connection = psycopg2.connect(**params)
            cur = connection.cursor()
            cur.execute("SELECT version()")
            db_version = cur.fetchone()
            cur.close()
            connection.close()
            connected = True
        except(Exception, psycopg2.DatabaseError) as error:
            ...
        
        return connected
    
    
    def disconnect(self):
        self.connection.close()
        self.connection = None

    
    def get_databases(self):
        connection = self.connect()
        cur = connection.cursor()

        query = "SELECT datname FROM pg_database WHERE datistemplate = false;"

        cur.execute(query)

        rows = cur.fetchall()

        cur.close()

        connection.close()

        return rows
    

    def get_database_tables(self, database=None):
        tables = None
        try:
            connection = self.connect(dbname=database)
            cur = connection.cursor()
            connection.autocommit = True
            query = f"SELECT tablename\
                    FROM pg_catalog.pg_tables\
                    WHERE schemaname = 'public';"
            cur.execute(query)

            rows = cur.fetchall()

            tables = []
            for row in rows:
                tables.append(row[0])

            cur.close()
            connection.close()

            self.table_names = tables
        except Error as e:
            self.raise_error(e, database_name=database)
        
        return tables

    def get_table_columns(self, table=None, current_database=None):
        if table is None:
            table = self.current_initial_table
        columns = None
        try:
            connection = self.connect(dbname=current_database)
            cur = connection.cursor()
            connection.autocommit = True
            query = f"SELECT * FROM {table} ;"
            cur.execute(query)

            rows = cur.fetchall()

            columns = [desc[0] for desc in cur.description]

            cur.close()
            connection.close()
            self.initial_table_column_names = columns
            
        except Error as e:
            self.raise_error(e, database_name=current_database)
        
        return columns
    
    def get_table_content(self, current_database=None):
        columns = None
        rows = None
        try:
            if self.current_initial_table is not None:
                connection = self.connect(dbname=current_database)
                cur = connection.cursor()
                connection.autocommit = True
                query = f"SELECT * FROM {self.current_initial_table} ;"
                cur.execute(query)

                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]

                cur.close()
                connection.close()
                self.initial_table_column_names = columns
                self.initial_table_rows = rows
                self.initial_table_rows_size = len(rows)
            else:
                columns = self.initial_table_column_names
                rows = self.initial_table_rows

            return columns, rows, len(rows)
        
        except Error as e:
            self.raise_error(e, database_name=current_database)
            return columns, rows, 0
        



    def create_new_database(self, database_name):
        connection = self.connect()
        cur = connection.cursor()
        connection.autocommit = True
        query = f"CREATE DATABASE {database_name} ;"
        cur.execute(query)
        cur.close()
        connection.close()


    def delete_database(self, database_name):
        try:
            connection = self.connect()
            cur = connection.cursor()
            connection.autocommit = True
            query = f"DROP DATABASE {database_name} ;"
            cur.execute(query)
            cur.close()
            connection.close()
        except Error as e:
            self.raise_error(e, database_name=database_name)


    @staticmethod
    def preprocess_name(name):
        for character in name:
            if character not in DBManager.syntax_valid_characters:
                name = name.replace(character, "")
        name = re.sub(r'\s+', '', name)
        return name

    @staticmethod
    def preprocess_columns_names(option_list):
        for name in option_list:
            name[0] = DBManager.preprocess_name(name[0])
        return option_list


    def create_new_table(self, table_name, option_list, csv_filename = None, current_database=None):
        connection = self.connect(dbname=current_database)
        cur = connection.cursor()
        connection.autocommit = True
        option_list = DBManager.preprocess_columns_names(option_list)
        columns = ", ".join(" ".join(y for y in x) for x in option_list)
        query = f"CREATE TABLE {table_name} ({columns}) ;"
        cur.execute(query)

        connection.commit()

        while not self.table_exists(table_name, cur):
            time.sleep(1)


        cur.close()
        connection.close()
        self.current_initial_table = table_name
        self.app.main_widget.widget(1).current_table = table_name
        

    def table_exists(self, table_name, cursor):
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = %s
            )
        """, (table_name,))
        return cursor.fetchone()[0]

    def delete_table(self, table_name, current_database=None):
        connection = self.connect(dbname=current_database)
        cur = connection.cursor()
        connection.autocommit = True
        query = f"DROP TABLE IF EXISTS {table_name} ;"

        cur.execute(query)

        cur.close()
        connection.close()
        iok = self.get_database_tables()
        if self.app.main_widget.widget(1).current_table == table_name:
            self.app.main_widget.widget(1).current_table = None
        if self.current_initial_table == table_name:
            self.current_initial_table = None
            self.initial_table_rows = None
            self.app.main_widget.widget(1).rebuild_table_widget()
        self.app.main_widget.widget(1).rebuild_db_tables_widget()
        self.app.main_widget.widget(1).current_database = current_database


    def create_new_rows_from_csv(self, table_name, columns, csv_filename, current_database=None):
        row_number = None
        try:
            connection = self.connect(dbname=current_database)
            cur = connection.cursor()
            connection.autocommit = True
            
            df = csv_manip.get_dataframe(csv_filename)
            
            values_list = df.values.tolist()

            column_names = [x[0] for x in columns]
            data_types = [x[1] for x in columns]
            column_names_string = ", ".join(column_names)

            for i, row in enumerate(values_list):
                values_list = []
                for ii, data_type in enumerate(data_types):
                    if "VARCHAR" in data_type or "CHAR" in data_type:
                        value = str(row[ii]).replace("'", "")
                        value = value.replace('"', '')
                        value = f"'{value}'"
                    else:
                        value = row[ii]
                    values_list.append(value)

                values_list = [str(x) for x in values_list]
                values = ", ".join(values_list)
                
                query = f"INSERT INTO {self.current_initial_table} ({column_names_string}) VALUES ({values}) ;"
                row_number = row
                cur.execute(query)
                connection.commit()

        except Error as e:
            parameters = (table_name, columns, csv_filename)
            self.raise_error(e, function=self.create_new_rows_from_csv, parameters=parameters, row_number=row_number)
            self.delete_table(table_name, current_database=current_database)


    def raise_error(self, e, function=None, parameters=None, row_number=None, database_name=None):
        self.app.raise_error(e, function, parameters, row_number, database_name)


    def create_new_row(self, inputs):
        connection = self.connect()
        cur = connection.cursor()
        connection.autocommit = True
        columns = ", ".join([colum for colum in list(inputs.keys())])
        values = [str("'" + value.text() + "'") if isinstance(value.text(), str) else value.text() for value in list(inputs.values())]
        values = ", ".join([value for value in values])
        query = f"INSERT INTO {self.current_initial_table} \
                ({columns})\
                VALUES ({values}) ;"
        cur.execute(query)

        cur.close()
        connection.close()
        self.initial_table_rows_size += 1
        self.get_table_columns()


    def delete_row(self, condition):
        connection = self.connect()
        cur = connection.cursor()
        connection.autocommit = True
        query = f"DELETE FROM {self.current_initial_table} \
                WHERE {condition} ;"
        cur.execute(query)
        
        cur.close()
        connection.close()
        if self.initial_table_rows_size > 0:
            self.initial_table_rows_size -= 0


    def slice_current_table(self, list_of_columns, condition, custom_select = None):
        connection = self.connect()
        columns = ", ".join(item for item in list_of_columns)
        if custom_select is not None:
            if len(list_of_columns) > 0:
                query = f"SELECT {columns}, {custom_select} FROM {self.current_initial_table}"
            else:
                
                query = f"SELECT {custom_select} FROM {self.current_initial_table}"
        else:
            query = f"SELECT {columns} FROM {self.current_initial_table}"
        
        where_condition = condition["WHERE"]
        group_by_condition = condition["GROUP BY"]
        having_condition = condition["HAVING"]
        if where_condition is not None:
            query += f" WHERE {where_condition}"
        if group_by_condition is not None:
            query += f" GROUP BY {group_by_condition}"
        if having_condition is not None:
            query += f" HAVING {having_condition}"
        query += ' ;'
        cur = connection.cursor()
        connection.autocommit = True
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        cur.close()
        connection.close()

        self.queried_list_of_columns = list_of_columns
        self.queried_table_column_names = columns
        self.queried_table_rows_size = len(rows)
        self.queried_table_rows = rows

        self.app.main_widget.widget(1).rebuild_table_widget(queried=True)


    def create_new_column(self, inputs, queried_table):
        connection = self.connect()
        cur = connection.cursor()
        connection.autocommit = True

        name = inputs["name"]
        data = inputs["data"]
        variable = inputs["variable"]
        constraints_input_keys = list(inputs.keys())
        constraints_input_keys.remove("name")
        constraints_input_keys.remove("data")
        constraints_input_keys.remove("variable")

        constraints_values = " ".join(inputs[value] for value in constraints_input_keys)

        query = f"ALTER TABLE {self.current_initial_table} ADD {name} {data} {constraints_values} DEFAULT {variable} ;"
                
        cur.execute(query)
        connection.commit()

        self.initial_table_column_names.append(name)

        cur.close()
        connection.close()


    def delete_column(self, input, queried_table):
        connection = self.connect()
        cur = connection.cursor()
        connection.autocommit = True

        query = f"ALTER TABLE {self.current_initial_table} DROP COLUMN {input} ;"

        self.initial_table_column_names.remove(input)
        cur.execute(query)
        connection.commit()
        cur.close()
        connection.close()


    def get_table_space(self, table_name):
        connection = self.connect()
        cur = connection.cursor()

        query = f"SELECT pg_size_pretty(pg_total_relation_size({table_name})) AS total_size;"

        cur.execute(query)

        output = cur.fetchall

        cur.close()
        connection.close()


    def get_table_width(self, table_name):
        connection = self.connect()
        cur = connection.cursor()

        query = f"SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '{table_name}' ;"
        
        cur.execute(query)

        width = cur.fetchone()[0]

        cur.close()
        connection.close()

        return width
    

    def get_table_height(self, table_name):
        connection = self.connect()
        cur = connection.cursor()

        query = f"SELECT COUNT(*) FROM {table_name} ;"
        cur.execute(query)

        height = cur.fetchone()[0]

        cur.close()
        connection.close()

        return height


    def get_table_size(self, table_name):
        connection = self.connect()
        cur = connection.cursor()

        query = f"SELECT COUNT(*) FROM information_schema.columns WHERE table_name = '{table_name}' ;"
        cur.execute(query)
        width = cur.fetchone()[0]

        query = f"SELECT COUNT(*) FROM {table_name} ;"
        cur.execute(query)
        height = cur.fetchone()[0]

        size = f"{width} x {height}"

        cur.close()
        connection.close()

        return size