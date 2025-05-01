# Imports
import pyodbc
from datetime import datetime
import pandas as pd


# Function to open/create database and ensure the table exists
# Full path to your MS Access database (.accdb) in r' format

class DatabaseTable:
    def __init__(self, database_path, table_name, fields):
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            rf'DBQ={database_path};'
        )
        conn = pyodbc.connect(conn_str)
        cur = conn.cursor()
        field_definitions = ['id AUTOINCREMENT PRIMARY KEY']
        for field_name, field_type in fields.items():
            field_definitions.append(f"{field_name} {field_type}")

        field_definitions_string = ', '.join(field_definitions)
        print(field_definitions_string)
        create_sql = f"CREATE TABLE {table_name} ({field_definitions_string})"

        try:
            cur.execute(create_sql)
            conn.commit()
            print('Table created successfully.')
        except Exception as e:
            print('Table already exists or another error:', e)

        self.conn = conn
        self.cur = cur
        self.fields = fields
        self.field_string = ', '.join(fields.keys())
        self.table_name = table_name

    # Function to add a new record
    def add_record(self, records):
        placeholders = ', '.join(['?'] * len(records))
        insert_sql = f"INSERT INTO {self.table_name} ({self.field_string}) VALUES ({placeholders})"

        try:
            self.cur.execute(insert_sql, records)
            self.conn.commit()
            print('Record added.')
        except Exception as e:
            print("Insert error:", e)

    def delete_record(self, field_name, value):
        """
        Deletes records where field_name == value.
        Use with care – this can delete multiple records if the field is not unique.
        """
        try:
            sql = f"DELETE FROM {self.table_name} WHERE {field_name} = ?"
            self.cur.execute(sql, (value,))
            self.conn.commit()
            print(f"Deleted record(s) where {field_name} = {value}")
        except Exception as e:
            print("Delete error:", e)

    def close_connection(self):
        self.cur.close()
        self.conn.close()


# --- MAIN PROGRAM ---

if __name__ == "__main__":
    # Full path to your MS Access database (.accdb)
    db_path = r'C:\Users\vasee\Downloads\lab09\ACS233\dtb.accdb'

    db_fields = {'[date]': 'TEXT', '[time]': 'TEXT', 'activity': 'TEXT', 'action': 'TEXT'}

    # Open the database
    logTable = DatabaseTable(db_path, 'log', db_fields)

    # Add a sample record
    logTable.add_record(['hello', 'hu', 'ds', 'dsds'])

    logTable.delete_record('id', 1)

    # Close the connection
    logTable.close_connection()
    print('Database connection closed.')
