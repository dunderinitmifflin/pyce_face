from tkinter import *
from tkinter import ttk


class RegistrationUI:
    def __init__(self, master):
        self.master = master
        master.title("Registration")

        mainframe = ttk.Frame(master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.label = Label(master, text="Fill out the required info")
        self.label.grid(column=2, row=1)

        self.first_name_label = Label(master, text="First Name: ")
        self.first_name_label.grid(column=1, row=2)

        self.last_name_label = Label(master, text="Last Name: ")
        self.last_name_label.grid(column=1, row=3)

        self.first_name_entry = Entry(master)
        self.first_name_entry.grid(column=2, row=2)

        self.last_name_entry = Entry(master)
        self.last_name_entry.grid(column=2, row=3)

        self.enter_button = Button(master, text="Enter", command=self.register)
        self.enter_button.grid(column=2, row=4)

    def register(self):
        print('{} {}'.format(self.first_name_entry.get(), self.last_name_entry.get()))


root = Tk()
my_gui = RegistrationUI(root)
root.mainloop()
