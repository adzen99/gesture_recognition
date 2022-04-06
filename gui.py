from tkinter import *
from tkinter import ttk
from options import Options

class GUI:
    def __init__(self, width=0, height=0, title=''):
        self.root = Tk()
        self.root.geometry(str(width)+'x'+str(height))
        self.root.resizable(False, False)
        self.root.title = title
    
    def create_button(self, text, cmd):
        button = ttk.Button(
            self.root,
            text = text,
            command = lambda : cmd(), 
        )
        button.pack(
            ipadx=5,
            ipady=5,
            expand=True
        )
        return button
    
    def options_popup(self):
        options = Options()
        options.show()


    def display_gui(self):
        self.create_button('Exit', self.root.quit)
        self.root.mainloop()