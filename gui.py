from tkinter import *
from tkinter import ttk
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
        popup = Tk()
        popup.geometry('600x400')
        popup.title('Options')
        label_sensitivity = Label(popup, text= "Cursor sensitivity")
        label_sensitivity.pack()
        w2 = ttk.Scale(popup, from_=0, to=10, orient=HORIZONTAL)
        w2.set(1)
        w2.pack()
        label_ = Label(popup, text= "Display hand landmarks")
        label_.pack()
        c = Checkbutton(popup, text = "Yes")
        c.pack()
        c = Checkbutton(popup, text = "Yes")
        c.pack()
        popup.mainloop()


    def display_gui(self):
        self.create_button('Exit', self.root.quit)
        self.root.mainloop()