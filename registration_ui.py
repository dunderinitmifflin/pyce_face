from tkinter import ttk, Label, Entry, Button, Tk
# from Pillow import Image, ImageTK


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

        self.email_label = Label(master, text="Email: ")
        self.email_label.grid(column=1, row=4)

        self.first_name_entry = Entry(master)
        self.first_name_entry.grid(column=2, row=2)

        self.last_name_entry = Entry(master)
        self.last_name_entry.grid(column=2, row=3)

        self.email_entry = Entry(master)
        self.email_entry.grid(column=2, row=4)

        self.enter_button = Button(master,
                                   text="Enter",
                                   command=self.register)
        self.enter_button.grid(column=2, row=5)

    def register(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        root.destroy()
        second_root = Tk()
        ConfirmationUI(second_root, first_name, last_name)
        second_root.mainloop()
        return first_name, last_name


class ConfirmationUI:
    def __init__(self, master, first_name, last_name):
        self.master = master
        master.title("Confirmation")
        master.minsize(300, 300)

        self.path = ""
        # self.image = ImageTK.PhotoImage(Image.open(path))
        # self.panel = Label(window, image=image)

        self.confirm_first_name = Label(master, text=first_name).grid(row=1)
        self.confirm_last_name = Label(master, text=last_name).grid(row=2)

        self.confirm_button = Button(master,
                                     text='Submit',
                                     command=self.confirm_register).grid(row=3)

    def confirm_register(self):
        pass


root = Tk()
my_gui = RegistrationUI(root)
root.mainloop()
