import face_recognition, pickle, cv2, os
from imutils import paths
 

def updateFaces():
    images = list(paths.list_images('Images')) # Stores list of all image paths in the 'Images' folder

    storedEncodings = []
    storedNames = []

    for (i, imagePath) in enumerate(images): 
        # Iterating over the paths

        name = imagePath.split(os.path.sep)[-2] 
        # Gets the name from the path 
        image = cv2.imread(imagePath) 
        # Reads the image into python using OpenCV
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb,model='hog')
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            storedEncodings.append(encoding) 
            # Adds encoding to list
            storedNames.append(name) 
            # Adds name to list

    data = {"encodings": storedEncodings, "names": storedNames}

    f = open("face_enc", "wb")
    f.write(pickle.dumps(data)) 
    # Writing data to file
    f.close()
    # Closing file 
updateFaces()