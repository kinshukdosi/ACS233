import sqlite3
import os
import pandas as pd
from datetime import datetime


class DatabaseTable:
    def __init__(self, database_path, table_name, fields):
        database_path = os.path.abspath(database_path)
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()
        self.table_name = table_name
        self.fields = fields

        field_definitions = ['id INTEGER PRIMARY KEY AUTOINCREMENT']
        for field_name, field_type in fields.items():
            field_definitions.append(f"{field_name} {field_type}")

        field_definitions_string = ', '.join(field_definitions)
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions_string})"

        try:
            self.cur.execute(create_sql)
            self.conn.commit()
            print('Table ensured/created successfully.')
        except Exception as e:
            print('Table creation error:', e)

        self.field_string = ', '.join(fields.keys())

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
        try:
            df = pd.read_sql_query(f"SELECT * FROM {self.table_name} WHERE {field_name} = ?", self.conn, params=(value,))
            if df.empty:
                print("Record doesn't exist and is not deleted")
            else:
                self.cur.execute(f"DELETE FROM {self.table_name} WHERE {field_name} = ?", (value,))
                self.conn.commit()
                print(f"Deleted record(s) where {field_name} = {value}")
        except Exception as e:
            print("Delete error:", e)

    def read_table(self):
        try:
            return pd.read_sql_query(f"SELECT * FROM {self.table_name}", self.conn)
        except Exception as e:
            print("Read error:", e)
            return pd.DataFrame()

    def delete_old_records(self, date_index):
        try:
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
                try:
                    date = datetime.strptime(record[1], '%d/%m/%y')
                    if date < cutoff_date:
                        self.cur.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (record[0],))
                        print(f"Deleted record ID {record[0]} dated {record[1]}")
                except Exception as date_error:
                    print(f"Date parse error on record {record}: {date_error}")

            self.conn.commit()
        except Exception as e:
            print("Delete old records error:", e)

    def close_connection(self):
        self.cur.close()
        self.conn.close()


# --- MAIN PROGRAM ---

if __name__ == "__main__":
    # Full path to your MS Access database (.accdb)
    db_path = r'securityRecords.db'

    db_fields = {'[Date]': 'TEXT', '[Time]': 'TEXT', 'Action': 'TEXT', 'Type': 'TEXT'}
    face_fields = {'Name': 'TEXT'}

    # Open the database
    logTable = DatabaseTable(db_path, 'log', db_fields)
    facetable = DatabaseTable(db_path, 'faces', face_fields)
    facetable.add_record(['Vasee'])


    # Add a sample record
    logTable.add_record(
        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Access granted', 'Level 2 access'])

    print(logTable.read_table())

    logTable.delete_old_records(0)

    # Close the connection
    logTable.close_connection()
