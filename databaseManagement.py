# Imports
import pyodbc
from datetime import datetime
import pandas as pd


# Function to open/create database and ensure the table exists
# Full path to your MS Access database (.accdb) in r' format
def open_database(database_path):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        rf'DBQ={database_path};'
    )
    conn = pyodbc.connect(conn_str)
    cur = conn.cursor()

    try:
        cur.execute("""CREATE TABLE log 
                    (id AUTOINCREMENT PRIMARY KEY, 
                     [date] TEXT, 
                     [time] TEXT, 
                     activity TEXT, 
                     action TEXT)""")
        conn.commit()
        print('Table created successfully.')
    except Exception as e:
        print('Table already exists or another error:', e)

    return conn, cur


# Function to add a new record
def add_to_database(conn, cur, activity_val, action_val):
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%y")
    formatted_time = now.strftime("%H:%M:%S")

    cur.execute("""INSERT INTO log ([date], [time], activity, action) 
                   VALUES (?, ?, ?, ?);""", (formatted_date, formatted_time, activity_val, action_val))
    conn.commit()
    print('Record added.')


# Function to export table to CSV
def export_to_csv(conn):
    try:
        df = pd.read_sql_query("SELECT * FROM log", conn)
        df.to_csv("log.csv", index=False)
        print('Exported to log.csv.')
    except Exception as e:
        print("Export error:", e)


# --- MAIN PROGRAM ---

if __name__ == "__main__":
    # Full path to your MS Access database (.accdb)
    database_path = r''

    # Open the database
    conn, cur = open_database(database_path)

    # Add a sample record
    add_to_database(conn, cur, 'Testing Activity', 'Started')

    # Export to CSV
    #export_to_csv(conn)

    # Close the connection
    cur.close()
    conn.close()
    print('Database connection closed.')
