import threading
import time
import pickle
from ffpyplayer.pic import Image as FFPImage


def load_frame_from_pickle(path: str) -> 'ffpyplayer.pic.Image':
    with open(path, 'rb') as f:
        data = pickle.load(f)

    # 3) rebuild the ffpyplayer.pic.Image
    img = FFPImage(
        data['planes'],
        pix_fmt   = data['pix_fmt'],
        size      = data['size'],

    )
    return img

class CAMERA_SIM:
    def __init__(self):
        self.name = None
        self.count = 0
        self.got_image = None


    def generate_image(self):
        while True:
            img = load_frame_from_pickle('obj2.bn')
            self.count = self.count + 1
            self.got_image(img, self.count)
            time.sleep(1)
    
    def start_cam_process(self):
        self.thread = threading.Thread(target=self.generate_image, daemon=True)

    def open_camera(self, id):
        self.name = id

    def play_camera(self):
        self.thread.start()


    def close_camera(self):
        print("Closing camera...")

    def stop_cam_process(self, join=False):
        exit() # only this is needed because the thread is daemonized




