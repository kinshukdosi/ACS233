import tkinter as tk
from tkinter import ttk
import sys
import time
from databaseManagement import DatabaseTable

from datetime import datetime

#class object for keypad
class keypad(tk.Frame):
    #constructor
    def __init__(self, master=None, key_callback=None, **kwargs):
        #inherits from tkinter import
        super().__init__(master, **kwargs)
        self.master = master
        self.key_callback = key_callback

        #General variables
        self.cursor = 2.0
        self.text_output = []
        self.entered_pin = []
        self.entered_name = []
        self.selector_mode = False
        self.enterring_name = False

        #System Variables
        self.access_level = 0
        self.system_mode = 'I'
        self.alarm_state = 'F'
        self.sector_triggered = "No sensor triggered"

        #calling methods to create window
        self.create_output_window()
        self.create_keypad()
        self.update_output_window()

        # starts time since last interaction
        self.interaction_time = time.time()

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
            'Face', '0', 'Del', 'Logout'
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
    
    #method called when a button is pressed, most text inputs are passed on to interface
    def key_pressed(self, text):
        self.interaction_time = time.time()
        #exits application
        if text == 'Exit':
            self.destroy()
            sys.exit()
        # handles empty button presses
        elif text == ' ':
            pass
        # handles logout button
        elif text == 'Logout':
            self.selector_mode = False
            self.key_callback(text)
        #moves cursor up when in menu    
        elif text == '^':
            if(self.cursor > 2):
                self.cursor -= 1.0
        #moves cursor down when in menu
        elif text == 'v':
            if(self.cursor < len(self.text_output)):
                self.cursor += 1.0
        #delete only deletes entries for pin
        elif text == 'Del':
            if self.entered_pin:
                self.entered_pin.pop()
        elif text == 'Face':
            self.key_callback(text)
        #handles enter button
        elif text == 'Ent':
            if(self.enterring_name): # if user was entering a name for adding it sends it with a prefix to interface and resets variable
                self.key_callback('N' + ''.join(self.entered_name))
                self.entered_name = []
            else:
                if(self.access_level == 0 and not(self.selector_mode)): # identifies pin entry then passes to interface and clears variable
                    self.key_callback(''.join(self.entered_pin))
                    self.entered_pin = []
                if(self.selector_mode): # identifies selecting an option for deleting then passes what the cursor was on to interface with a prefix
                    self.key_callback("D" + str(self.text_output[int(self.cursor)-1]))
                else:
                    try: # attempts to pass what the cursor was on to interface
                        self.key_callback(str(self.text_output[int(self.cursor)-1]))
                    except IndexError:
                        print("Nothing selected")
        else:
            # both are for the number keys and adds them to the correct variable
            if(self.enterring_name):
                self.entered_name.append(text)
            else:
                self.entered_pin.append(text)

    #creates output window inside main window as a text box
    def create_output_window(self):
        self.output_window = tk.Text(self, height=10, width = 50, bg='black', fg='white', relief = 'raised')
        self.output_window.grid(row = 0, column =0, rowspan=4)
        self.sensor_triggered_window = tk.Text(self, height=1, width=50, bg='black', fg='white', relief = 'raised')
        self.sensor_triggered_window.grid(row = 11, column = 0, rowspan = 4)
        

    #updates output window by clearing window then reprinting the text_output variable
    #also adds cursor when in menu
    def update_output_window(self):
        temp_text_output = self.text_output # stores text so it can be checked if it has changed later

        if(not(self.selector_mode)): # checks system is not selecting a name for deleting
            if(self.access_level == 0): # identifies pin entry mode
                self.text_output = ["Enter pin:", ]
                for i in self.entered_pin:
                    self.text_output.append('*') # shows user star instead of pin numbers
            # shows user options for access level 2, options vary based on system state
            elif(self.access_level == 1):
                if(self.system_mode == 'D'):
                    self.text_output = ['Level 1 accessed\n', '1.Switch to night mode\n']
                else:
                    self.text_output = ['Level 1 accessed\n', '1.Switch to day mode\n']
            # identifies access level 2
            elif(self.access_level == 2):
                if(self.enterring_name): # checks if user is enterring a name for adding a face
                    self.text_output = ["Enter user ID: ", self.entered_name]
                # shows options for level 2 access
                else:
                    if(self.system_mode == 'D'):
                        self.text_output =['Level 2 accessed\n', '1.Switch to night mode\n', '2.Add face\n', '3.Delete face\n', '4.Deactivate system\n', '5.change pin\n', '6.Export log to csv']
                    else:
                        self.text_output =['Level 2 accessed\n', '1.Switch to day mode\n', '2.Add face\n', '3.Delete face\n', '4.Deactivate system\n', '5.change pin\n', '6.Export log to csv']

        # if text has been changed resets cursor to initial position
        if(temp_text_output != self.text_output):
            self.cursor = 2.0


        current_time = datetime.now().time() # resets time of last interaction
        self.output_window.delete('1.0', tk.END) # deletes text in output window
        i = 0
        # adds currently correct text back in
        for line in self.text_output:
            if i == 0:
                self.output_window.insert(tk.END, current_time.strftime('%H:%M') + ' ' + line)
                i = 1
            else: 
                self.output_window.insert(tk.END, line)
        # adds cursor whilst checking it is not outside bounds of selectable text
        if int(self.cursor) < (len(self.text_output) + 1):
            self.output_window.tag_add('highlightline', f"{int(self.cursor)}.0", f"{int(self.cursor+1.0)}.0")
        self.output_window.tag_config('highlightline', background = "white", foreground = 'black')

        self.sensor_triggered_window.delete('1.0', tk.END)
        self.sensor_triggered_window.insert(tk.END, self.decode_sensor(self.sector_triggered))
        self.after(10, self.update_output_window)

    # function decodes the identification code that the arduino passes over when the alarm is triggered for displaying to user
    def decode_sensor(self, code):
        if(code != "No sensor triggered"):
            output = ""
            if(code[:3] == "REC"):
                output = "Reception "
            elif(code[:3] == "GAL"):
                output = "Gallery "
            
            if(code[4:7] == "LED"):
                return ""
            elif(code[4:7] == "CAS"):
                output = output + "case "
            elif(code[4:7] == "BUT"):
                output = output + "panic button "
            elif(code[4:7] == "PAI"):
                output = output + "painting "
            elif(code[4:7] == "DOO"):
                output = output + "door "
            elif(code[4:7] == "WIN"):
                output = output + "window "
            elif(code[4:7] == "PIR"):
                output = output + "motion sensor "

            output = output + code[8]
            return output
        else:
            return code