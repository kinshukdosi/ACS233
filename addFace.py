import cv2, os, datetime
from updateFaces import updateFaces
import sqlite3
import pandas as pd


def startVideo(cameraID):
    ''' Checks video is valid, requires a cameraID argument.
    Returns False if invalid and returns the video object if valid '''

    video = cv2.VideoCapture(cameraID)
    if video.isOpened() == False:  # .isOpened() checks if the video is available
        print(f'Camera with ID {cameraID} not detected')
        return False
    return video


def captureFace(name, frame):
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()

    # Check if name already exists in the table
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

    if not os.path.exists(f"Images/{ID}"):  # Create folder for user ID if it doesn't exist
        os.makedirs(f"Images/{ID}")

    # Create a filename without illegal characters
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    imageFilePath = f"Images/{ID}/{timestamp}.png"

    print(f"Saving image to: {imageFilePath}")
    success = cv2.imwrite(imageFilePath, frame)  # Save the image to disk
    print("Success:", success)


def startAddFace(cameraID, name):
    video = startVideo(cameraID)
    if not video:
        return
    while True:
        ret, frame = video.read()
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirror view
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit loop on 'q'
            break
        if key == ord('c'):  # Capture image on 'c'
            captureFace(name, frame)
            print(f"Added face for {name}!")
            break

    video.release()  # Release the camera resource
    cv2.destroyAllWindows()  # Close all OpenCV windows
