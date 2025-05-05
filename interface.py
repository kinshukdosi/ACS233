import IKeypad
from IKeypad import keypad
import tkinter as tk
from databaseManagement import DatabaseTable
from datetime import datetime
import facialRecognition, addFace, deleteFace, updateFaces
import time
import serial

'''
 Function takes a text input and directs functionality based on the text input 
 This function is mainly used by the keypad object as the function called by
 a button being pressed, where the button text will then be passed to this function.
'''
def keypad_selection(text):
    # Checks if the text sent is for a pin attempt and ignores any other button, then sends to arduino
    if(keypad.access_level == 0 and text != 'Face' and text != 'Del' and text != '^' and text != 'Ent' and text != 'v' and text != 'Logout' and text[0] != '*'):
        serial_write(arduino, 'p' + text)
    else:
        #checks if face button has been pressed while in access level 1 which is the only state the button should function
        if(keypad.access_level == 1 and text == 'Face'):
            valid_face_id, face_id_num = facialRecognition.start(0) # calls facial recognition to start then stores returned values
            # checks if a face was identified
            if face_id_num != []:
                # checks if it was a known face
                if face_id_num[0] != 'Unknown':
                    # retrieves name associated with face
                    face_id_name = deleteFace.get_face_name(face_id_num[0])[0]
                    if valid_face_id:
                        serial_write(arduino, 'f') # tells arduino that face check was successfull
                        # adds a log of face id
                        logTable.add_record(
                            [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Access Level 2 granted',
                            face_id_name])
            else:
                # adds log of failed facial recognition attempt
                logTable.add_record(
                        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Access Level 2 failed',
                        '-'])
        # handles logout button      
        elif(text == 'Logout'):
            # adds logout to log
            logTable.add_record(
                        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Logged out', '-'])
            serial_write(arduino, 'a0') # tells arduino to return to access level 0
        
        # handles when face for deleting has been selected
        elif text.strip()[0] == 'D':
            name = text.strip()[1:] # strips prefix
            id = deleteFace.get_face_ID(name) # retrieves file id
            deleteFace.deleteFace(id) # calls function that deletes face
            name = deleteFace.get_face_name(id) # retrieves name for log
            updateFaces.updateFaces() # calls function to update database
            # adds deletion to log
            logTable.add_record(
                [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Face Deleted', name])
            keypad.selector_mode = False # returns keypad from selector mode
        
        # handles add face choice
        elif text.strip()[0] == '2':
            # sets keypad to wait for a name for the face to be entered
            keypad.enterring_name = True

        # handles when a name for adding the face has been entered
        elif text.strip()[0] == 'N':
            name = text.strip()[1:]
            addFace.startAddFace(0, name) # starts the face capture
            updateFaces.updateFaces() # updates databases
            logTable.add_record(
                [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Face Added', name])
            keypad.enterring_name = False # returns keypad from enterring name mode
        
        # identifies user selection of delete face
        elif text.strip()[0] == '3':
            get_face_del()
        
        # identifies export log selection
        elif text.strip()[0] == '6':
            logTable.export_to_csv()
        else:
            message = get_selection_message(text) # checks if text passed needs formatting before being sent to the arduino
            if(message != None): # if text was not recognised for formatting None is returned
                serial_write(arduino, message)
            else:
                print("Unknown selection" + text)

# This function formats messages that can be sent directly to arduino without other processes
def get_selection_message(selection):
    # identifies mode change selection
    if selection.strip()[0] == '1':
        if(keypad.system_mode == 'D'):
            return "mN" # message to arduino is mode Night
        else:
            return "mD" # message to arduino is mode Day
    # identifies idle mode aka deactivate system
    elif selection.strip()[0] == '4':
        return "mI" # message to arduino is mode Idle
    # identifies 
    elif selection.strip()[0] == '5':
        return "changePin"
    # returns none if it is not recognised
    else:
        return None

# function handles setting the keypad for face deleting and retrieving names for keypad
def get_face_del():
    try:
        names = [name + '\n' for name in deleteFace.get_all_names()]
        names.insert(0, "Select a face to be deleted (Logout to exit this screen)\n")
    except FileNotFoundError:
        names = ["No image files found\n"]
    keypad.selector_mode = True
    keypad.text_output = names


# function writes input string to serial communication
def serial_write(arduino, message):
    toArdu = '<' + str(message) + '>' # adds characters so the arduino knows where message starts and ends
    print("Message to Arduino: " + toArdu)
    if(arduino != None):
        arduino.write(bytes(toArdu, 'utf-8'))

# function checks for messages from arduino and handles the message
def serial_check_resp(arduino):
    # checks if last interaction was within 30 seconds otherwise logs out
    if (time.time() - keypad.interaction_time) > 30:
        serial_write(arduino, 'a0')

    if(arduino != None):
        # checks if message is waiting
        if arduino.in_waiting > 0:
            raw_response = arduino.read_until()
            response = raw_response.decode().strip()

            # Response from the serial communication
            if response:
                #print("Response from arduino: " + response)

                # Current access level is added to keypad
                if response[0] == 'a':
                    keypad.access_level = int(response[1])

                # Current Mode is added to keypad
                elif response[0] == 'm':
                    if keypad.system_mode != response[1]:
                        keypad_selection('Logout')
                        match response[1]:
                            case 'I':
                                log_str = 'Changed to Idle'
                            case 'N':
                                log_str = 'Changed to Night mode'
                            case _:
                                log_str = 'Changed to Day mode'
                        logTable.add_record(
                            [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Changed mode',
                            log_str])
                    keypad.system_mode = response[1]

                # Current Alarm state is added to keypad
                elif response[0] == 't':
                    if keypad.alarm_state != response[1] and response[1] == 'F':
                        logTable.add_record(
                            [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Deactivated Alarm',
                            '-'])
                        
                        keypad.sector_triggered = "No sensor triggered"
                        print("Reset alarm trigger")
                        
                    keypad.alarm_state = response[1]

                # Sensor triggered is added to keypad
                elif response[0] == 's':
                    keypad.sector_triggered = response[1:]
                    logTable.add_record(
                        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Alarm Activated',
                        response[1:]])

                # Pin check result is added to log
                elif response[0] == 'p':
                    # Pin is wrong 3 times
                    if response[1] == 'F':
                        logTable.add_record(
                            [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Alarm Activated',
                            'Pin entered wrong 3 times'])
                    # Pin is correct
                    elif response[1] == 's':
                        logTable.add_record(
                            [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"),
                            'Access Level 1 granted', '-'])
                        print(response)
                    
                    # Clears entered pin after attempt
                    if response[1] == 'f' or response[1] == 'F':
                        keypad.entered_pin = []

            else:
                print("empty response")
    

    # function is called every 10ms 
    root.after(10, lambda: serial_check_resp(arduino))

# establishes connection to arduino
def connect_arduino():
    print("Connecting to arduino")
    try:
        print("attempting connection...")
        arduino = serial.Serial(port = 'COM5', baudrate = 9600)
        print("connection successful")
        return arduino
    except serial.SerialException as e:
        print("Error: Arduino not found")

# safely closes keypad and ends connection with arduino while returning access level to 0
def shutdown_procedure():
    root.destroy()
    if arduino:
        serial_write(arduino, 'a0')
        arduino.close()

# function calls itself once a day to clear old records
def clean_old_records():
    logTable.delete_old_records(0)

    root.after(86400000, clean_old_records)

# when file is ran starts processes
if __name__ == "__main__":

    # Starting arduino comms
    arduino = connect_arduino()

    # Prep database
    # Creates a database object
    db_fields = {'[Date]': 'TEXT', '[Time]': 'TEXT', 'Action': 'TEXT', 'Type': 'TEXT'}
    logTable = DatabaseTable(r'securityRecords.db', 'log', db_fields)


    # Starting up interface
    print("starting interface")

    root = tk.Tk()
    keypad = IKeypad.keypad(root, key_callback=keypad_selection)
    keypad.pack(padx=20, pady=20) # starts keypad window
    clean_old_records() # starts old record clearing
    serial_check_resp(arduino) # starts checking for arduino messages
    print("Response checked")
    root.protocol("WM_DELETE_WINDOW", shutdown_procedure) # sets keypad to safely close when window is shut
    root.mainloop()