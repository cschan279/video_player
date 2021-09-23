import time
from threading import Thread, Event
from tkinter.filedialog import askopenfilename
import ui
import capture


def get_n_show():
    global cap
    r, f = cap.get_frame()
    if r:
        root.display.updateFrame(f)
        curr_t = cap.get_current_index()/ cap.fps
        root.curr_var.set(round(curr_t,2))

def playVideo():
    global root, cap, stop_event
    while not stop_event.is_set():
        if root.pause_event.is_set():
            time.sleep(0.1)
        else:
            get_n_show()
            time.sleep(cap.interval)
            root.scroll_var.set(cap.get_current_index())

def set_time_pos(index):
    global root, cap
    cap.set_current_index(index)
    get_n_show()


def ask_for_file():
    global root, cap, stop_event
    filename = askopenfilename()
    if not filename:
        return
    stop_event.set()
    root.pause_event.set()
    root.pause_btn.configure(text=">")
    time.sleep(0.1)
    root.title(filename)
    cap = capture.Capture(filename)
    root.scroll.configure(to=cap.length)
    root.tot_var.set(round(cap.duration, 2))
    get_n_show()
    stop_event.clear()
    Thread(target=playVideo).start()
    




if __name__ == "__main__":
    stop_event = Event()
    cap = None
    root = ui.MainWindow()
    root.cap_btn.configure(command=ask_for_file)
    root.scroll.configure(command=set_time_pos)
    root.mainloop()
    stop_event.set()