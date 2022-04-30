from tkinter import *
from tkinter import ttk
import tkinter
import dotenv
import os

class Options:
    def __init__(self):
        self.root_options = Tk();
        self.root_options.title('Options')

        self.sensitivity = None
        self.display_landmarks = None
        self.var = None
    def show(self):

        dotenv.load_dotenv()

        Label(self.root_options, text= "Cursor sensitivity").grid(row=0, column=0)
        self.sensitivity = ttk.Scale(self.root_options, from_=1, to=10, orient=HORIZONTAL)
        self.sensitivity.set(os.environ['MOUSE_SENSITIVITY'])

        self.sensitivity.grid(row=1, column=0)

        self.var = IntVar()
        self.var.set(str(os.environ['DISPLAY_LANDMARKS']))
        Label(self.root_options, text= "Display hand landmarks").grid(row=2, column=0)
        Radiobutton(
            self.root_options,
            text = 'Yes',
            variable = self.var,
            value = 1,
            command=lambda: print(self.var.get())).grid(row=3, column=0)

        Radiobutton(
            self.root_options,
            text = 'No',
            variable = self.var,
            value = 2,
            command=lambda: print(self.var.get())).grid(row=3, column=1)

        ttk.Button(self.root_options, text="Cancel", command=self.root_options.quit).grid(row=4, column=0)
        ttk.Button(self.root_options, text="Save", command=self.save).grid(row=4, column=1)

        self.root_options.mainloop()

    def save(self):
        dotenv.set_key(dotenv.find_dotenv(), "MOUSE_SENSITIVITY", str(self.sensitivity.get()))
        dotenv.set_key(dotenv.find_dotenv(), "DISPLAY_LANDMARKS", str(self.var.get()))
        