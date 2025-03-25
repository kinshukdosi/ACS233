import tkinter as tk
from tkinter import ttk

class keypad(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.accessGranted = False
        
        self.create_keypad()
        self.updateOutput("Enter pin: ")

    def updateOutput(self, text):
        self.outputWindow.insert(0.0, text)
    

    def create_keypad(self):
                            
        style = ttk.Style()
        style.configure('keypad.TButton', padding=10, relief="raised")
        
        self.outputWindow = tk.Text(self, bg='black', fg='white', height=12, width=50, relief="raised")
        self.outputWindow.grid(row=0, column=0, rowspan=4)

        pad = [
            '1', '2', '3', '^',
            '4', '5', '6', 'Ent',
            '7', '8', '9', 'v',
            'Yes', '0', 'No', ' '
            ]

        row, col = 0, 10
        for button_text in pad:
            button = ttk.Button(self, text=button_text, style='keypad.TButton', command = lambda text=button_text: self.key_pressed(text))
            button.grid(row=row, column=col, padx=5, pady=5)
            col+=1
            if col>13:
                col=10
                row+=1
    

    def key_pressed(self, text):
        if text == "Yes":
            pass
        elif text == 'No':
            pass
        elif text == 'Ent':
            pass
        elif text == ' ':
            pass
        elif text == '^':
            pass
        elif text == 'v':
            pass
        else:
            if(self.accessGranted):
                pass
            else:
                self.outputWindow.insert(tk.END, "*")

if __name__ == "__main__":
    root = tk.Tk()
    keypad = keypad(root)
    keypad.pack(padx=20, pady=20)
    root.mainloop()
