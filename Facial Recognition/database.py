import sqlite3

def viewDatabase():
    '''Function to create the database if it does not exist'''
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            ID INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def getListOfIDs():
    '''Function to get list of IDs present in the database'''
    IDs = []
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM people')

    rows = cursor.fetchall()
    
    for row in rows:
        IDs.append(row[0])
    
    conn.commit()
    conn.close()
    return IDs

def getListOfNames():
    '''Function to get list of names present in the database'''
    names = []
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM people')

    rows = cursor.fetchall()

    for row in rows:
        names.append(row[1])
    
    conn.commit()
    conn.close()
    return names

viewDatabase()
IDs = getListOfIDs()
names = getListOfNames()

print(IDs, names)