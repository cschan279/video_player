from tkinter import StringVar, Tk, Scale, Frame, Canvas, Label, Button, IntVar
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from threading import Event
import cv2


class VideoCanvas(Canvas):
    def __init__(self, parent, width=1280, height=720):
        Canvas.__init__(self, parent, width=width, height=height, border=1, relief='solid')
        self.default_image = self.blankImage(width, height)
        self.display = self.create_image(0, 0,
                                        image=self.default_image, 
                                        anchor='nw')
        self.image = self.blankImage(width, height)
        pass
        
    def get_size(self):
        return self.winfo_width(), self.winfo_height()

    def blankImage(self, width=None, height=None):
        if width and height:
            size=(width, height)
        else:
            size = self.get_size()
        img = Image.new('RGB', size, color='blue')
        return ImageTk.PhotoImage(img)

    def updateFrame(self, cvImg):
        size = self.get_size()
        img = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
        self.image = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.itemconfig(self.display, image=self.image)
        return

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.display = VideoCanvas(self, width=1280, height=720)
        self.display.grid(row=0, column=0, columnspan=3, sticky="news")
        self.scroll_var = IntVar()
        self.scroll = Scale(self, from_=0, to=0, resolution=1,
                            variable=self.scroll_var, orient='horizontal', showvalue=False)
        self.scroll.grid(row=1, column=0, columnspan=4, sticky="ew")
        self.scroll.columnconfigure(0, weight=1)

        self.pause_btn = Button(self, text=">", command=self.pause_cmd, width=2)
        self.pause_btn.grid(row=2, column=0, sticky='w')

        self.curr_var, self.tot_var = StringVar(), StringVar()
        self.curr_lbl = Label(self, textvariable=self.curr_var)
        self.curr_lbl.grid(row=2, column=1)
        self.tot_lbl = Label(self, textvariable=self.tot_var)
        self.tot_lbl.grid(row=2, column=2)
        self.pause_event = Event()
        self.pause_event.set()
        self.cap_btn = Button(self, text="file")
        self.cap_btn.grid(row=2, column=3, sticky='w')
        return

    def pause_cmd(self):
        if self.pause_event.is_set():
            self.pause_event.clear()
            self.pause_btn.configure(text="||")
        else:
            self.pause_event.set()
            self.pause_btn.configure(text=">")

    def ask_for_file(self):
        self.filename = askopenfilename()
        self.title(self.filename)

        

