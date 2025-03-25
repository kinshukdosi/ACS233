import tkinter as tk
from tkinter import ttk

class keypad(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.access_granted = False
        self.text_output = ['Enter pin:']
        self.PASSKEY = ['1', '2', '3', '4']
        self.LEVEL_1_OPTIONS = ['Level 1 accessed\n', 'Switch between day/night\n']
        self.LEVEL_2_OPTIONS = ['Add face\n', 'Delete face\n', 'Deactivate system\n', 'change pin (not entry pin)\n']
        self.entered_pin = []
        self.cursor = 2.0

        self.create_output_window()
        self.create_keypad()
        self.update_output_window()
    

    def create_keypad(self):
        style = ttk.Style()
        style.configure('keypad.TButton', padding=10, relief="raised")

        pad = [
            '1', '2', '3', '^',
            '4', '5', '6', 'Ent',
            '7', '8', '9', 'v',
            'Face', '0', ' ', 'Del'
            ]

        row, col = 0, 10
        for button_text in pad:
            button = ttk.Button(self, text=button_text, style='keypad.TButton', command = lambda text=button_text: self.key_pressed(text))
            button.grid(row=row, column=col)
            col+=1
            if col>13:
                col=10
                row+=1
    

    def key_pressed(self, text):
        if text == " ":
            pass
        elif text == 'Face':
            if(self.access_granted):
                self.level_2_access()
        elif text == 'Ent':
            if not(self.access_granted):
                if self.entered_pin == self.PASSKEY:
                    self.access_granted = True
                    self.text_output = self.LEVEL_1_OPTIONS
            else:
                print(f'User Selected: {self.text_output[int(self.cursor)-1]}')
        elif text == 'Del':
            if not(self.access_granted):
                if len(self.entered_pin) > 0:
                    self.entered_pin.pop()
                    self.text_output.pop()
                    self.update_output_window()
                
            
        elif text == '^':
            if(self.cursor > 2):
                self.cursor -= 1.0
        elif text == 'v':
            if(self.cursor < len(self.text_output)):
                self.cursor += 1.0
        else:
            if(self.access_granted):
                pass
            else:
                self.text_output.append('*')
                self.entered_pin.append(text)

        self.update_output_window()

    def create_output_window(self):
        self.output_window = tk.Text(self, height=10, width = 50, bg='black', fg='white', relief = 'raised')
        self.output_window.grid(row = 0, column = 0, rowspan=4)

    def update_output_window(self):
        self.output_window.delete('1.0', tk.END)
        for line in self.text_output:
            self.output_window.insert(tk.END, line)

        if(self.access_granted):
            self.output_window.tag_add('highlightline', self.cursor, self.cursor+1.0)
            self.output_window.tag_config('highlightline', background = "white", foreground = 'black')

    def level_2_access(self):
        self.text_output = self.LEVEL_1_OPTIONS + self.LEVEL_2_OPTIONS
        self.text_output[0] = 'level 2 accessed\n'
        self.update_output_window()
            

if __name__ == "__main__":
    root = tk.Tk()
    keypad = keypad(root)
    keypad.pack(padx=20, pady=20)
    root.mainloop()
