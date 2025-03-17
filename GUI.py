import tkinter as tk
from tkinter import ttk

class keypad(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.output_screen = ttk.Entry(self, state='readonly')
        self.output_screen.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky='ew')
        
        self.create_keypad()

    def create_keypad(self):
        style = ttk.Style()
        style.configure('keypad.TButton', padding=10, relief="raised")

        pad = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'Yes', '0', 'No'
            ]

        row, col = 1, 0
        for button_text in pad:
            button = ttk.Button(self, text=button_text, style='keypad.TButton', command = lambda text=button_text: self.key_pressed(text))
            button.grid(row=row, column=col, padx=5, pady=5)
            col+=1
            if col>2:
                col=0
                row+=1

    def key_pressed(self, text):
        current_text = self.output_screen.get()
        if text == "Yes":
            self.output_screen.config(state='normal')
            self.output_screen.delete(0, tk.END)
            self.output_screen.config(state='readonly')
        elif text == 'No':
            self.output_screen.config(state='normal')
            self.output_screen.delete(0, tk.END)
            self.output_screen.config(state='readonly')
        else:
            self.output_screen.config(state='normal')
            self.output_screen.delete(0, tk.END)
            self.output_screen.insert(0, current_text + text)
            self.output_screen.config(state='readonly')

if __name__ == "__main__":
    root = tk.Tk()
    keypad = keypad(root)
    keypad.pack(padx=20, pady=20)
    root.mainloop()
