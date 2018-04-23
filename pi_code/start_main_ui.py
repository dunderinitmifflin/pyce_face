from tkinter import ttk, Label, Entry, Button, Tk
import os


class Start:
    def __init__(self, master):
        self.master = master
        master.title = 'Start Registration'
        
        self.start_button = Button(master,
                                   text='Start Registration',
                                   command=self.start_registration)
        
        self.start_button.pack()
        
    def start_registration(self):
        os.system('python3 ui_tk_5.py')
        

root = Tk()
my_gui = Start(root)
root.mainloop()