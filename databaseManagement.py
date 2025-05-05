# Import necessary libraries
import sqlite3  # For working with SQLite databases
import os  # For handling file paths
import pandas as pd  # For exporting data to CSV
from datetime import datetime  # For working with dates and times


# Define a class to manage a table within an SQLite database
class DatabaseTable:
    def __init__(self, database_path, table_name, fields):
        # Convert database path to absolute path
        database_path = os.path.abspath(database_path)

        # Connect to the SQLite database (creates it if it doesn't exist)
        self.conn = sqlite3.connect(database_path)
        self.cur = self.conn.cursor()  # Create a cursor object to execute SQL commands

        self.table_name = table_name  # Store the table name
        self.fields = fields  # Store the field definitions (column names and types)

        # Start defining SQL to create table (with an auto-incrementing 'id' primary key)
        field_definitions = ['id INTEGER PRIMARY KEY AUTOINCREMENT']

        # Add user-specified fields to the table definition
        for field_name, field_type in fields.items():
            field_definitions.append(f"{field_name} {field_type}")

        # Join all field definitions into a single string
        field_definitions_string = ', '.join(field_definitions)

        # Final SQL command to create the table if it doesn't already exist
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions_string})"

        # Execute the SQL command
        self.cur.execute(create_sql)
        self.conn.commit()  # Save (commit) the changes

        # Prepare a string of just the field names (excluding 'id') for later use
        self.field_string = ', '.join(fields.keys())

    # Method to insert a new record into the table
    def add_record(self, records):
        # Create a placeholder string like "?, ?, ?, ..." based on the number of fields
        placeholders = ', '.join(['?'] * len(records))

        # Prepare the SQL insert statement
        insert_sql = f"INSERT INTO {self.table_name} ({self.field_string}) VALUES ({placeholders})"

        # Execute the insert statement with the provided values
        self.cur.execute(insert_sql, records)
        self.conn.commit()  # Save changes

    # Method to delete records older than 7 months based on a date field
    def delete_old_records(self, date_index):
        today = datetime.now()  # Get the current date
        month = today.month - 7  # Go back 7 months
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        # Determine the cutoff date
        cutoff_date = datetime(year, month, today.day)

        # Retrieve all records with their 'id' and date field (based on the given index)
        self.cur.execute(f"SELECT id, {list(self.fields.keys())[date_index]} FROM {self.table_name}")
        records = self.cur.fetchall()

        # Loop through the records and delete any that are older than the cutoff date
        for record in records:
            # Parse the date string into a datetime object (expects format dd/mm/yy)
            date = datetime.strptime(record[1], '%d/%m/%y')
            if date < cutoff_date:
                self.cur.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (record[0],))

        self.conn.commit()  # Save deletions

    # Method to export the entire table to a CSV file
    def export_to_csv(self):
        # Read the entire table into a Pandas DataFrame
        data = pd.read_sql_query(f"SELECT * FROM {self.table_name}", self.conn)
        # Export the DataFrame to a CSV file with the table name
        data.to_csv(self.table_name + ".csv", index=False)

    # Method to properly close the database connection
    def close_connection(self):
        self.cur.close()  # Close the cursor
        self.conn.close()  # Close the connection to the database
