import tkinter as tk
from tkinter import ttk
import sys
import serial

from datetime import datetime
import time

class keypad(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.access_granted = False

        self.arduino = serial.Serial(port = 'COM5', baudrate=9600)
        
        self.entered_pin = []
        self.text_output = ['Enter pin:']

        self.create_output_window()
        self.create_keypad()
        self.update_output_window()

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

        #creates output window inside main window as a text box
    def create_output_window(self):
        self.output_window = tk.Text(self, height=10, width = 50, bg='black', fg='white', relief = 'raised')
        self.output_window.grid(row = 0, column =0, rowspan=4)

    #Updates output window with text stored in text_output
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

    def key_pressed(self, text):
        # Deals with blank buttons
        if text == " ":
            pass
        # Button for face id communication needs finishing
        elif text == 'Face':
            pass
        # Enter button deals with most communication and selects from cursor
        elif text == 'Ent':
            self.enter_pressed()

        # Deletes entries for pin
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

    def access_attempt(self):
        self.serial_write(''.join(self.entered_pin))
        response = self.serial_check_resp()
        if(response.strip() == "access_granted"):
            print("Access granted")
            self.access_granted = True
            self.level_1_access()

    #method writes input string to serial communication
    def serial_write(self, message):
        toArdu = '<' + str(message) + '>'
        self.arduino.write(bytes(toArdu, 'utf-8'))

    def serial_check_resp(self):
        raw_response = self.arduino.read_until()
        response = raw_response.decode()
        if(response == "access_denied"):
            access_granted = False
        return response


    def level_1_access(self):
        self.text_output = self.LEVEL_1_OPTIONS
        self.logTable.add_record([datetime.now().strftime("%d/%m/%y"), datetime.now().strftime("%H:%M:%S"), 'Access granted', 'Level 2 access'])
        self.update_output_window()

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
