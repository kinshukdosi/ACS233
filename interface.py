import IKeypad
import tkinter as tk

import serial

def keypad_selection(text):
    print(text)
    if(keypad.access_level == 0):
        serial_write(arduino, 'p' + text)
    else:
        serial_write(arduino, get_selection_message(text))


def get_selection_message(selection):
    if selection.strip()[1] == '1':
        return "mD"
    elif selection.strip()[1] == '2':
        return "addF"
    elif selection.strip()[1] == '3':
        return "delF"
    elif selection.strip()[1] == '4':
        return "deactSys"
    elif selection.strip()[1] == '5':
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
        if response:
            print("Response from arduino: " + response)
            print(type(response))

            if response[0] == 'a':
                keypad.access_level = int(response[1])
                print(f"current access level: {keypad.access_level}")
            if response[0] == 'm':
                keypad.system_mode = response[1]
                print(f"current system mode: {keypad.system_mode}")
            


            

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