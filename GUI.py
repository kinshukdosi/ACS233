import tkinter as tk
from tkinter import ttk
import serial
import sys

from databaseManagement import DatabaseTable
from datetime import datetime
import time


#class object for keypad
class keypad(tk.Frame):
    #constructor
    def __init__(self, master=None, **kwargs):
        #inherits from tkinter import
        super().__init__(master, **kwargs)
        self.master = master

        #sets up serial connection with arduino
        self.arduino = serial.Serial(port = 'COM5', baudrate=9600)

        #General variables
        self.access_granted = False
        self.pin_entry_screen()
        self.LEVEL_1_OPTIONS = ['Level 1 accessed\n', 'Switch between day/night\n']
        self.LEVEL_2_OPTIONS = ['Add face\n', 'Delete face\n', 'Deactivate system\n', 'change pin\n']
        self.entered_pin = []
        self.cursor = 2.0

        #calling methods to create window
        self.create_output_window()
        self.create_keypad()
        self.update_output_window()

        #Initialises Log database
        db_fields = {'[Date]': 'TEXT', '[Time]': 'TEXT', 'Activity': 'TEXT', 'Action': 'TEXT'}
        self.logTable = DatabaseTable(r'securityRecords.accdb', 'Log', db_fields)

    #function currently not used, kept in case of implementation of searching arduino port instead of hard coding
    def find_arduino(port=None):
        if port is None:
            ports = serial.tools.list_ports.comports()
            for p in ports:
                if p.manufacturer is not None and "Arduino" in p.manufacturer:
                    port = p.device

        print(port)
        return port
    
    #method writes input string to serial communication
    def serial_write(self, message):
        toArdu = '<' + str(message) + '>'
        print("Message to Arduino: " + toArdu)
        self.arduino.write(bytes(toArdu, 'utf-8'))

    def serial_check_resp(self):
        raw_response = self.arduino.read_until()
        response = raw_response.decode()
        print("Response from arduino: " + response)
        print(type(response))

        # Sensor is tripped
        if response.strip()[0] == 's':
            sensor_name = response.strip()[1:]
            self.logTable.add_record(
                [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Alarm activated',
                 sensor_name])

        # Pin is wrong 3 times
        elif response.strip()[0] == 'p':
            self.logTable.add_record(
                [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Alarm activated',
                 'Pin wrong too many times'])

        # System is timed out
        if(response.strip() == "timeOut"):
            print("returning to log in screen")
            self.access_granted = False
            self.logTable.add_record(
                [datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Logged out', 'Time out'])
            self.pin_entry_screen()
        return response
        
    
    #method creates keypad
    def create_keypad(self):
        #defines button style
        style = ttk.Style()
        style.configure('keypad.TButton', padding=10, relief="raised")

        #array holding text for each button
        pad = [
            '1', '2', '3', '^',
            '4', '5', '6', 'Ent',
            '7', '8', '9', 'v',
            'Face', '0', 'Del', 'Exit'
            ]

        #iterates through to place buttons starting on column 10 to make room for output window
        row, col = 0, 10
        for button_text in pad:
            button = ttk.Button(self, text=button_text, style='keypad.TButton', command = lambda text=button_text: self.key_pressed(text))
            button.grid(row=row, column=col)
            col+=1
            if col>13:
                col=10
                row+=1
    
    def access_attempt(self):            
        self.serial_write(''.join(self.entered_pin))
        response = self.serial_check_resp()
        if(response.strip() == "access_granted"):
            print("Access granted worked")
            self.access_granted = True
            self.text_output = self.LEVEL_1_OPTIONS
            self.logTable.add_record([datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Level 1 access', '-'])
        else:
            print("access_granted failed")
            print(type(response))

    #method called when a button is pressed
    def key_pressed(self, text):
        #for blank buttons
        if text == " ":
            pass
        #activates facial recognition
        #in this form of the code it just goes directly to level 2 if user has gotten passed the pin
        elif text == 'Face':
            if(self.access_granted):
                self.level_2_access()
                self.logTable.add_record([datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Access granted', 'Level 2 access'])
        #deals with enter button
        #button is used for both entering the pin and selecting options from menu
        elif text == 'Ent':
            if not(self.access_granted):
                self.access_attempt()
            else:
                self.serial_write(self.get_selection_message(str(self.text_output[int(self.cursor)-1])))
                self.logTable.add_record([datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), str(self.text_output[int(self.cursor)-1]), '-'])
                print("waiting for response...")
                response = self.serial_check_resp()
                    
                    
                    
        #delete only deletes entries for pin
        elif text == 'Del':
            if not(self.access_granted):
                if len(self.entered_pin) > 0:
                    self.entered_pin.pop()
                    self.text_output.pop()
                    self.update_output_window()
        
        #moves cursor up when in menu    
        elif text == '^':
            if(self.cursor > 2):
                self.cursor -= 1.0
        #moves cursor down when in menu
        elif text == 'v':
            if(self.cursor < len(self.text_output)):
                self.cursor += 1.0

        #exits application and closes connection to arduino
        elif text == 'Exit':
            self.arduino.close()
            root.destroy()
            sys.exit()
        #deals with number key pressses
        else:
            if(self.access_granted):
                pass
            else:
                self.text_output.append('*')
                self.entered_pin.append(text)
        #updates output window after each button press
        self.update_output_window()

    #creates output window inside main window as a text box
    def create_output_window(self):
        self.output_window = tk.Text(self, height=10, width = 50, bg='black', fg='white', relief = 'raised')
        self.output_window.grid(row = 0, column =0, rowspan=4)

    #updates output window by clearing window then reprinting the text_output variable
    #also adds cursor when in menu
    def update_output_window(self):
        current_time = datetime.now().time()
        self.output_window.delete('1.0', tk.END)
        i = 0
        for line in self.text_output:
            if i == 0:
                self.output_window.insert(tk.END, current_time.strftime('%H:%M') + ' ' + line)
                i = 1
            else: 
                self.output_window.insert(tk.END, line)

        if(self.access_granted):
            self.output_window.tag_add('highlightline', self.cursor, self.cursor+1.0)
            self.output_window.tag_config('highlightline', background = "white", foreground = 'black')

    def pin_entry_screen(self):
        self.text_output = ['Enter pin:']


    #possibly temporary method to show level 2 options
    def level_2_access(self):
        self.text_output = self.LEVEL_1_OPTIONS + self.LEVEL_2_OPTIONS
        self.text_output[0] = 'level 2 accessed\n'
        self.update_output_window()

    def get_selection_message(self, selection):
        if selection.strip() == 'Switch between day/night':
            return "switchDN"
        elif selection.strip() == 'Add face':
            return "addF"
        elif selection.strip() == 'Delete face':
            return "delF"
        elif selection.strip() == 'Deactivate system':
            return "deactSys"
        elif selection.strip() == 'change pin':
            return "changePin"
        else:
            return selection


    def check_comms(self):
        if self.arduino.in_waiting:
            self.serial_check_resp()

        root.after(100, self.check_comms)

#causes object to be created when the program is ran
if __name__ == "__main__":
    root = tk.Tk()
    keypad = keypad(root)
    keypad.pack(padx=20, pady=20)
    print(keypad.logTable.read_table())
    keypad.check_comms()
    root.mainloop()
