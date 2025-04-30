import tkinter as tk
from tkinter import ttk
import serial

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
        arduino = serial.Serial(port = find_arduino, baudrate=9600)

        #General variables
        self.access_granted = False
        self.text_output = ['Enter pin:']
        self.PASSKEY = ['1', '2', '3', '4']
        self.LEVEL_1_OPTIONS = ['Level 1 accessed\n', 'Switch between day/night\n']
        self.LEVEL_2_OPTIONS = ['Add face\n', 'Delete face\n', 'Deactivate system\n', 'change pin (not entry pin)\n']
        self.entered_pin = []
        self.cursor = 2.0

        #calling methods to create window
        self.create_output_window()
        self.create_keypad()
        self.update_output_window()

    def find_arduino(port=None):
        if port is None:
            ports = serial.tools.list_ports.comports()
            for p in ports:
                if p.manufacturer is not None and "Arduino" in p.manufacturer:
                    port = p.device
        return port
    
    #method writes input string to serial communication
    def serial_write(self, message):
        toArdu = '<' + str(message) + '>'
        arduino.write(bytes(toArdu, 'utf-8'))

    def serial_check_resp(self):
        raw_response = arduino.read_until()
        response = raw.decode()
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
            'Face', '0', ' ', 'Del'
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
        #deals with enter button
        #button is used for both entering the pin and selecting options from menu
        elif text == 'Ent':
            if not(self.access_granted):
                serial_write(self.entered_pin)
                response = serial_check_resp()
                if(response = "access_granted")
                    self.access_granted = True
                
            else:
                print(f'User Selected: {self.text_output[int(self.cursor)-1]}')
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

    #possibly temporary method to show level 2 options
    def level_2_access(self):
        self.text_output = self.LEVEL_1_OPTIONS + self.LEVEL_2_OPTIONS
        self.text_output[0] = 'level 2 accessed\n'
        self.update_output_window()
            
#causes object to be created when the program is ran
if __name__ == "__main__":
    root = tk.Tk()
    keypad = keypad(root)
    keypad.pack(padx=20, pady=20)
    root.mainloop()
