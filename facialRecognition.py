import cv2, face_recognition, pickle, os
import sqlite3


cascPathface = os.path.dirname(
 cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPathface)
data = pickle.loads(open('face_enc', "rb").read()) # Face encodings of previously stored images of people
noInput = cv2.imread('noInput.png')


def startVideo(cameraID):
    ''' Checks video is valid, requires a cameraID argument.
    Returns False if invalid and returns the video object if valid '''

    video = cv2.VideoCapture(cameraID)
    if video.isOpened() == False: # .isOpened() checks if the video is available
        print(f'Camera with ID {cameraID} not detected')
        return False
    return video

def analyseFrame(video):
    '''Analyses video for faces, compares with known encodings, and draws boxes with names.'''
    
    if not isinstance(video, cv2.VideoCapture):
        print('Video object is invalid')
        return None 

    ret, frame = video.read()
    if not ret or frame is None:
        return None

    frame = cv2.flip(frame, 1)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Speed up encoding by shrinking image
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small, model='hog')  # faster model
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    names = []

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matched_ids = [data["names"][i] for i, matched in enumerate(matches) if matched]
            name = max(set(matched_ids), key=matched_ids.count)

        names.append(name)

    # Scale back up face locations since we detected on the smaller image
    for (top, right, bottom, left), name in zip(face_locations, names):
        # Scale to original frame size
        top, right, bottom, left = [coord * 4 for coord in (top, right, bottom, left)]

        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        label = f"Employee ID: {name}" if name != "Unknown" else "UNKNOWN"

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, label, (left + 10, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        if name == "Unknown":
            alert()  # Still call alert if unknown

    return frame

def alert():
    print("Alert!!!!") 
    

def start(cameraID):
    video = startVideo(cameraID)
    while True:
        frame = analyseFrame(video=video)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

start(1)