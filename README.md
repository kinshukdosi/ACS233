# ACS233 Burglar Alarm System
This is where we should talk about
Configuration instructions.
Installation instructions.
Operating instructions.
A file manifest (a list of files in the directory or archive)
Copyright and licensing information.
Contact information for the distributor or author.
A list of known bugs.
Troubleshooting instructions.

<b>Facial Recognition Setup</b><br/>
Required Python Libraries: opencv-python, face_recognition, pickle, os<br/>
Create "Images" folder within the same directory<br/>
Create a folder within /Images/ for each person to be added to the database e.g. Images/Kinshuk/ or /Images/Jamie/<br/>
Run updateFaces.py
Run facialRecognition.py, making sure the final line of code start() includes the correct camera ID for the webcam that you wish to use<br/>

