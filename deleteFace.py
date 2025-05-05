import os  # File system operations
import sqlite3  # SQLite database handling
import updateFaces  # Updates facial recognition data after changes

# Deletes image files and database record for a given ID
def deleteFace(ID):
    path = f"Images/{ID[0]}"
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        print(filename, "is removed")
    os.rmdir(path)

    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM people WHERE ID = ?', (ID[0],))
    conn.commit()
    conn.close()

    updateFaces.updateFaces()
    print(f"Faces with ID {ID} removed from system")

# Returns the name of a person using their ID
def get_face_name(ID):
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM people WHERE ID = ?', (ID[0],))
    name = cursor.fetchone()
    conn.close()
    return name

# Returns the ID of a person using their name
def get_face_ID(name):
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ID FROM people WHERE name = ?', (name,))
    ID = cursor.fetchone()
    conn.close()
    return ID

# Returns a list of all names in the database
def get_all_names():
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM people')
    fetched_names = cursor.fetchall()
    conn.close()

    names = []
    for item in fetched_names:
        names.append(item[0])
    return names
