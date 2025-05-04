import IKeypad
from IKeypad import keypad
import tkinter as tk
from databaseManagement import DatabaseTable
from datetime import datetime

import serial

def keypad_selection(text):
    print(text)
    if(keypad.access_level == 0):
        serial_write(arduino, 'p' + text)
    else:
        serial_write(arduino, get_selection_message(text))


def get_selection_message(selection):
    if selection.strip()[0] == '1':
        if(keypad.system_mode == 'D'):
            return "mN"
        else:
            return "mD"
    elif selection.strip()[0] == '2':
        return "addF"
    elif selection.strip()[0] == '3':
        return "delF"
    elif selection.strip()[0] == '4':
        return "deactSys"
    elif selection.strip()[0] == '5':
        return "changePin"
    else:
        return selection


#method writes input string to serial communication
def serial_write(arduino, message):
    toArdu = '<' + str(message) + '>'
    print("Message to Arduino: " + toArdu)
    arduino.write(bytes(toArdu, 'utf-8'))


def serial_check_resp(arduino):
    if arduino.in_waiting > 0:
        raw_response = arduino.read_until()
        response = raw_response.decode().strip()

        # Response from the serial communication
        if response:
            print("Response from arduino: " + response)

            # Current access level
            if response[0] == 'a':
                keypad.access_level = int(response[1])

            # Current Mode
            elif response[0] == 'm':
                if keypad.access_level != response[1]:
                    match response[1]:
                        case 'I':
                            log_str = 'Changed to Idle'
                        case 'N':
                            log_str = 'Changed to Night mode'
                        case _:
                            log_str = 'Changed to Day mode'
                    keypad.logTable.add_record(
                        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Changed mode',
                         log_str])
                keypad.system_mode = response[1]

            # Current Alarm state
            elif response[0] == 't':
                if keypad.alarm_state != response[1] and response[1] == 'F':
                    keypad.logTable.add_record(
                        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Deactivated Alarm',
                         '-'])
                keypad.alarm_state = response[1]

            # Sensor triggered
            elif response[0] == 's':
                keypad.logTable.add_record(
                    [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Alarm Activated',
                     response[1:]])

            # Pin check result
            elif response[0] == 'p':
                # Pin is wrong 3 times
                if response[1] == 'F':
                    keypad.logTable.add_record(
                        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Alarm Activated',
                         'Pin entered wrong 3 times'])
                # Pin is correct
                elif response[1] == 's':
                    keypad.logTable.add_record(
                        [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"),
                         'Access Level 1 granted', '-'])

        else:
            print("empty response")


    
    root.after(250, lambda: serial_check_resp(arduino))

def connect_arduino():
    print("Connecting to arduino")
    try:
        print("attempting connection...")
        arduino = serial.Serial(port = 'COM5', baudrate = 9600)
        print("connection successful")
        return arduino
    except serial.SerialException as e:
        print("Error: Arduino not found")

if __name__ == "__main__":
    # Starting arduino comms
    arduino = connect_arduino()

    # Starting up interface
    print("starting interface")

    root = tk.Tk()
    keypad = IKeypad.keypad(root, key_callback=keypad_selection)
    keypad.pack(padx=20, pady=20)
    serial_check_resp(arduino)
    print("Response checked")
    root.mainloop()
    arduino.close()