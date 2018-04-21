from tkinter import ttk, Label, Entry, Button, Tk
from PIL import Image, ImageTk
from send_pic_to_register import take_pic, send_pic, insert_new_face_into_db, get_files, turn_on_one_led_or_none
from time import sleep
import os
directory = '/home/pi/camera/'
from get_rek_id import search_faces
##from main_registration import start_tkinter

pin_green = 13
pin_yellow = 6
pin_red = 5


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
        email = self.email_entry.get()
        root.destroy()
        take_pic()
        second_root = Tk()
        ConfirmationUI(second_root, first_name, last_name, email)
        second_root.mainloop()
##        return first_name, last_name, email


class ConfirmationUI:
    def __init__(self, master, first_name, last_name, email):
        self.master = master
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        master.title("Confirmation")
        master.minsize(300, 300)
        
        list_of_jpgs = get_files(directory)
        image_path = '{}{}'.format(directory, list_of_jpgs[0])
        print(image_path)
        
        image_temp = Image.open(image_path)
        image_temp = image_temp.resize((250, 250), Image.ANTIALIAS)
        
        self.image = ImageTk.PhotoImage(image_temp)
        self.panel = Label(master, image=self.image).pack()

        self.confirm_first_name = Label(master, text=first_name).pack()
        self.confirm_last_name = Label(master, text=last_name).pack()
        self.confirm_email = Label(master, text=email).pack()


        self.confirm_button = Button(master,
                                     text='Submit',
                                     command=self.confirm_register).pack()

    def confirm_register(self):
        print('you just clicked the submit button')
        send_pic()
        rekognition_id = search_faces()
        # run a search for that same picture
        insert_new_face_into_db(self.first_name,
                                self.last_name,
                                self.email,
                                rekognition_id)
        self.master.destroy()
        turn_on_one_led_or_none(pin_green)
        sleep(2)
        turn_on_one_led_or_none()
        
##        root = Tk()
##        my_gui = RegistrationUI(root)
##        root.mainloop()

root = Tk()
my_gui = RegistrationUI(root)
root.mainloop()



##print('1')
##root = Tk()
##print('2')
##my_gui = RegistrationUI(root)
##print('3')
##root.mainloop()
##print('4')
