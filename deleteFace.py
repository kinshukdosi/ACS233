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


