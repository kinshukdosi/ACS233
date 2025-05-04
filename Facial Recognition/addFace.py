import cv2, os, datetime
from updateFaces import updateFaces
import sqlite3

def startVideo(cameraID):
    ''' Checks video is valid, requires a cameraID argument.
    Returns False if invalid and returns the video object if valid '''

    video = cv2.VideoCapture(cameraID)
    if video.isOpened() == False: # .isOpened() checks if the video is available
        print(f'Camera with ID {cameraID} not detected')
        return False
    return video

def captureFace(name, frame):
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM people WHERE name = ? LIMIT 1', (name,))
    result = cursor.fetchone()
    if result:
        cursor.execute('SELECT ID FROM people WHERE name = ?', (name,))
    else:
        cursor.execute('INSERT INTO people (name) VALUES (?)', (name,))
        cursor.execute('SELECT ID FROM people WHERE name = ?', (name,))

    ID = cursor.fetchone()
    ID = ID[0]
    conn.commit()
    conn.close()

    if not os.path.exists(f"Images/{ID}"):
        os.mkdir(f"Images/{ID}")
    imageFilePath = f"Images/{ID}/{datetime.datetime.now()}.png"
    cv2.imwrite(imageFilePath, frame)



def startAddFace(cameraID, name):
    video = startVideo(cameraID)
    if not video:
        return
    while True:
        ret, frame = video.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('c'):
            captureFace(name, frame)
            print(f"Added face for {name}!")
            break


cameraID = 1
startAddFace(cameraID, "Vasee")
updateFaces()

