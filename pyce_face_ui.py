from __future__ import print_function
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
import threading
import datetime
import imutils
import cv2
import os


class RegistrationUI:
    def __init__(self, vs, output_path):
        self.master = master
        master.title("Registration")
        self.vs = vs
        self.output_path = output_path
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.panel = None
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

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.root.wm_title("PyImageSearch PhotoBooth")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def register(self):
        print('{} {}'.format(self.first_name_entry.get(), self.last_name_entry.get()))

    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)

                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tkinter.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def takeSnapshot(self):
        # grab the current timestamp and use it to construct the
        # output path
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.outputPath, filename))

        # save the file
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(filename))

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

# root = Tk()
# my_gui = RegistrationUI(root)
# root.mainloop()
