from tkinter import *
from tkinter import ttk
from tkinter.ttk import Label, Style
import dotenv
import os

from keyboard_controller import KeyboardController
from mouse_controller import MouseController
from calculator_controller import CalculatorController

class GUI:
    def __init__(self, width=0, height=0, title=''):
        self.root = Tk()
        self.root.title('Gestures controller')
        self.root.geometry(str(width)+'x'+str(height))
        self.root.resizable(False, False)
        self.root.title = title
        self.sensitivity = None
        self.var = None
    
    def create_button(self, text, cmd, frame):
        button = ttk.Button(
            frame,
            text = text,
            command = lambda: cmd(), 
        )
        return button

    def display_gui(self):
        
        dotenv.load_dotenv()

        frame= Frame(self.root, relief= 'sunken')
        frame.grid(sticky= "we")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        l = Label(frame, text= "Options")
        l.config(font=(23))
        l.grid(row=0, column=0)
        Label(frame, text= "Cursor sensitivity").grid(row=1, column=0)
        self.sensitivity = ttk.Scale(frame, from_=1, to=10, orient=HORIZONTAL, command=lambda x=None: dotenv.set_key(dotenv.find_dotenv(), "MOUSE_SENSITIVITY", str(self.sensitivity.get())))
        self.sensitivity.set(os.environ['MOUSE_SENSITIVITY'])

        self.sensitivity.grid(row=2, column=0)

        self.var = IntVar()
        self.var.set(os.environ['DISPLAY_LANDMARKS'])

        Label(frame, text= "Display hand landmarks").grid(row=3, column=0)

        Radiobutton(
            frame,
            text = 'Yes',
            variable = self.var,
            value = 1,
            command=lambda x=None: dotenv.set_key(dotenv.find_dotenv(), "DISPLAY_LANDMARKS", str(self.var.get()))).grid(row=4, column=0)

        Radiobutton(
            frame,
            text = 'No',
            variable = self.var,
            value = 0,
            command=lambda x=None: dotenv.set_key(dotenv.find_dotenv(), "DISPLAY_LANDMARKS", str(self.var.get()))).grid(row=5, column=0)

        mouse_controller = MouseController()
        keyboard_controller = KeyboardController()
        calculator_controller = CalculatorController()

        self.create_button('Mouse controller', mouse_controller.actions, frame).grid(row=6, column=0, pady=10)
        self.create_button('Keyboard controller', keyboard_controller.create_keyboard, frame).grid(row=7, column=0, pady=10)
        self.create_button('Calculator controller', calculator_controller.display, frame).grid(row=8, column=0, pady=10)

        self.create_button('Exit', self.root.quit, frame).grid(row=9, column=0, pady=10)
        self.root.mainloop()