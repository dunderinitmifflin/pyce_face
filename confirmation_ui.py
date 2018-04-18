from registration_ui import RegistrationUI
from tkinter import *
from tkinter import ttk
from Pillow import Image, ImageTK


class ConfirmationUI:
    def __init__(self, master):
        self.master = master
        mainframe = ttk.Frame(master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        path = ""
        image = ImageTK.PhotoImage(Image.open(path))
        panel = tkinter.Label(window, image=image)

        