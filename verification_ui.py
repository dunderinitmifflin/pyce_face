from tkinter import Button, Tk


class VerificationUI:
    def __init__(self, master):
        self.master = master
        master.title('Verfication')

        verify_button = Button(master, text='Verify', command=self.verify)
        verify_button.pack()

    def verify(self):
        pass


root = Tk()
my_gui = VerificationUI(root)
root.mainloop()
