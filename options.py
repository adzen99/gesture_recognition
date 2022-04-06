from tkinter import *
from tkinter import ttk
import tkinter
import dotenv
import os

class Options:
    def __init__(self):
        self.root = Tk();
        # self.root.geometry('600x400')
        self.root.title('Options')
        self.options = {}

    def clicked(self, r):
        # self.options['MOUSE_SENSITIVITY'] = self.var.get()
        print(r)

    def show(self):

        dotenv.load_dotenv()

        Label(self.root, text= "Cursor sensitivity").grid(row=0, column=0)
        sensitivity = ttk.Scale(self.root, from_=0, to=10, orient=HORIZONTAL)
        sensitivity.set(os.environ['MOUSE_SENSITIVITY'])

        sensitivity.grid(row=1, column=0)

        self.options['MOUSE_SENSITIVITY'] = sensitivity.get()
        r = IntVar()
        r.set("2")
        Label(self.root, text= "Display hand landmarks").grid(row=2, column=0)
        ttk.Radiobutton(self.root, text = "Yes", variable=r, value=1, command=lambda: self.clicked(r.get())).grid(row=3, column=0)
        ttk.Radiobutton(self.root, text = "No", variable=r, value=2, command=lambda: self.clicked(r.get())).grid(row=3, column=1)
        ttk.Button(self.root, text="Cancel").grid(row=4, column=0)
        ttk.Button(self.root, text="Save", command=self.save).grid(row=4, column=1)
        self.root.mainloop()

    def save(self):
        # print(self.options)
        pass