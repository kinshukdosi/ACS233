import sys
import os


import IKeypad
from IKeypad import keypad
import tkinter as tk
from databaseManagement import DatabaseTable
from datetime import datetime
import facialRecognition, addFace, deleteFace
import updateFaces
import time
import serial

def keypad_selection(text):
    print(text)
    if(keypad.access_level == 0 and text != 'Face' and text != 'Del' and text != '^' and text != 'Ent' and text != 'v' and text != 'Logout' and text[0] != '*'):
        serial_write(arduino, 'p' + text)
    else:
        if(keypad.access_level == 1 and text == 'Face'):
            valid_face_id, face_id_num = facialRecognition.start(0)
            face_id_name = deleteFace.get_face_name(face_id_num[0])[0]
            if valid_face_id:
                serial_write(arduino, 'f')
                logTable.add_record(
                    [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Access Level 2 granted',
                    face_id_name])
                 
        elif(text == 'Logout'):
            logTable.add_record(
                        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Logged out', '-'])
            serial_write(arduino, 'a0')
            
        elif text.strip()[0] == 'D':
            name = text.strip()[1:]
            id = deleteFace.get_face_ID(name)
            deleteFace.deleteFace(id)
            name = deleteFace.get_face_name(id)
            updateFaces.updateFaces()
            logTable.add_record(
                [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Face Deleted', name])
            keypad.selector_mode = False
            
        elif text.strip()[0] == '2':
            keypad.enterring_name = True

        elif text.strip()[0] == 'N':
            name = text.strip()[1:]
            addFace.startAddFace(0, name)
            updateFaces.updateFaces()
            logTable.add_record(
                [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Face Added', name])
            keypad.enterring_name = False
            
        elif text.strip()[0] == '3':
            get_face_del()
        
        elif text.strip()[0] == '6':
            logTable.export_to_csv()
        else:
            message = get_selection_message(text)
            if(message != None):
                serial_write(arduino, message)
            else:
                print("Unknown selection" + text)


def get_selection_message(selection):
    if selection.strip()[0] == '1':
        if(keypad.system_mode == 'D'):
            return "mN"
        else:
            return "mD"
    elif selection.strip()[0] == '4':
        return "mI"
    elif selection.strip()[0] == '5':
        return "changePin"
    else:
        return None

def get_face_del():
    try:
        names = [name + '\n' for name in deleteFace.get_all_names()]
        names.insert(0, "Select a face to be deleted (Logout to exit this screen)\n")
    except FileNotFoundError:
        names = ["No image files found\n", "Exit\n"]
    keypad.selector_mode = True
    keypad.text_output = names


#method writes input string to serial communication
def serial_write(arduino, message):
    toArdu = '<' + str(message) + '>'
    print("Message to Arduino: " + toArdu)
    if(arduino != None):
        arduino.write(bytes(toArdu, 'utf-8'))


def serial_check_resp(arduino):
    if (time.time() - keypad.interaction_time) > 30:
        serial_write(arduino, 'a0')

    if(arduino != None):
        if arduino.in_waiting > 0:
            raw_response = arduino.read_until()
            response = raw_response.decode().strip()

            # Response from the serial communication
            if response:
                #print("Response from arduino: " + response)

                # Current access level
                if response[0] == 'a':
                    keypad.access_level = int(response[1])

                # Current Mode
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

                # Current Alarm state
                elif response[0] == 't':
                    if keypad.alarm_state != response[1] and response[1] == 'F':
                        logTable.add_record(
                            [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Deactivated Alarm',
                            '-'])
                        
                        keypad.sector_triggered = "No sensor triggered"
                        print("Reset alarm trigger")
                        
                    keypad.alarm_state = response[1]

                # Sensor triggered
                elif response[0] == 's':
                    keypad.sector_triggered = response[1:]
                    logTable.add_record(
                        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Alarm Activated',
                        response[1:]])

                # Pin check result
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
    

    
    root.after(10, lambda: serial_check_resp(arduino))

def connect_arduino():
    print("Connecting to arduino")
    try:
        print("attempting connection...")
        arduino = serial.Serial(port = 'COM5', baudrate = 9600)
        print("connection successful")
        return arduino
    except serial.SerialException as e:
        print("Error: Arduino not found")

def shutdown_procedure():
    root.destroy()
    if arduino:
        serial_write(arduino, 'a0')
        arduino.close()

def clean_old_records():
    logTable.delete_old_records(0)

    root.after(86400000, clean_old_records)

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
    keypad.pack(padx=20, pady=20)
    clean_old_records()
    serial_check_resp(arduino)
    print("Response checked")
    root.protocol("WM_DELETE_WINDOW", shutdown_procedure)
    root.mainloop()