import os, sqlite3
import updateFaces

def deleteFace(ID):
    path = f"Images/{ID}"
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        print(filename, "is removed")
    os.rmdir(path)
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM people WHERE ID = ?', (ID,))

    conn.commit()
    conn.close()
    updateFaces.updateFaces()
    print(f"Faces with ID {ID} removed from system")


def get_face_name(ID):
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM people WHERE ID = ?', (ID,))
    name = cursor.fetchone()
    conn.close()
    return name

def get_face_ID(name):
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ID FROM people WHERE name = ?', (name,))
    ID = cursor.fetchone()
    conn.close()
    return ID

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