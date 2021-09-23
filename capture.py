import cv2

class Capture:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        assert self.cap.isOpened()
        c_index = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        self.codec = "".join([chr((c_index>>i)&0xFF) for i in range(0,32,8)])
        self.fps = round(self.cap.get(cv2.CAP_PROP_FPS),2)
        assert self.fps
        self.interval = (1/self.fps)*0.95
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.length / self.fps
        print(self.codec, self.fps, self.interval, self.duration)
        self.index = self.get_current_index()

    def get_current_index(self):
        return self.cap.get(cv2.CAP_PROP_POS_FRAMES)

    def set_current_index(self, index):
        return self.cap.set(cv2.CAP_PROP_POS_FRAMES, int(index))

    def get_frame(self):
        return self.cap.read()


if __name__ == "__main__":
    p = Capture("r1.mp4")
