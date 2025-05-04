# Imports
import pyodbc
import os
import pandas as pd
from datetime import datetime
# Function to open/create database and ensure the table exists
# Full path to your MS Access database (.accdb) in r' format


class DatabaseTable:
    def __init__(self, database_path, table_name, fields):
        database_path = os.path.abspath(database_path)
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
            record_to_delete = pd.read_sql_query(f"SELECT * FROM {self.table_name} WHERE {field_name} = ?", self.conn,params=(value,))

            if record_to_delete.empty:
                print("Record doesn't exist and is not deleted")

            else:
                sql = f"DELETE FROM {self.table_name} WHERE {field_name} = ?"
                self.cur.execute(sql, (value,))
                self.conn.commit()
                print(f"Deleted record(s) where {field_name} = {value}")

        except Exception as e:
            print("Delete error:", e)

    def read_table(self):
        try:
            data = pd.read_sql_query(f"SELECT * FROM {self.table_name}", self.conn)
            return data
        except Exception as e:
            print("Read error:", e)
            return pd.DataFrame()

    def delete_old_records(self, date_index):
        today = datetime.now()
        month = today.month - 7
        year = today.year

        if month <= 0:
            month += 12
            year -= 1

        cutoff_date = datetime(year, month, today.day)

        self.cur.execute(f"SELECT id, {list(self.fields.keys())[date_index]} FROM {self.table_name}")
        records = self.cur.fetchall()

        for record in records:
            date = datetime.strptime(record[1], '%d/%m/%y')
            if date < cutoff_date:
                self.cur.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (record[0],))
                print(f"Deleted record ID {record[0]} dated {record[1]}")

        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()


# --- MAIN PROGRAM ---

if __name__ == "__main__":
    # Full path to your MS Access database (.accdb)
    db_path = r'securityRecords.accdb'

    db_fields = {'[Date]': 'TEXT', '[Time]': 'TEXT', 'Action': 'TEXT', 'Type': 'TEXT'}
    face_fields = {'Name': 'TEXT'}

    # Open the database
    logTable = DatabaseTable(db_path, 'log', db_fields)
    facetable = DatabaseTable(db_path, 'faces', face_fields)
    #facetable.add_record(['Vasee'])


    # Add a sample record
    logTable.add_record(
        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Access granted', 'Level 2 access'])

    print(logTable.read_table())

    logTable.delete_old_records(0)

    # Close the connection
    logTable.close_connection()

    print(facetable.read_table())
    facetable.close_connection()