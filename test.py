from tkinter import *

root = Tk()

r = IntVar()
r.set("2")

Radiobutton(root, text="option 1", variable=r, value=1, command=lambda: print(r.get())).grid(row=0, column=0)
Radiobutton(root, text="option 2", variable=r, value=2, command=lambda: print(r.get())).grid(row=0, column=1)

root.mainloop()