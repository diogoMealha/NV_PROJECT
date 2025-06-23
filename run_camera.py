# file related to simulation
from thorcam.camera import ThorCam

import time
import numpy as np
import utils.functions_file as ff

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import queue

CAM_IMG_SIZE = (2048, 2448)  # 
MAG_BASELINE = np.zeros(CAM_IMG_SIZE)
#global IMAGE_LIST
IMAGE_LIST = []

class MyThorCam(ThorCam):


    # def __init__(self):
    #     global MAG_BASELINE
    def received_camera_response(self, msg, value):
        super(MyThorCam, self).received_camera_response(msg, value)
        if msg == 'image':
            return
        print('Received "{}" with value "{}"'.format(msg, value))
    def got_image(self, image, count, queued_count, t):
        image_data = image_to_bytes(image)
        image_queue.put(image_data)
        
        if count > 500:
            exit()
        
        if count < 100:
            global MAG_BASELINE
            MAG_BASELINE = image_data.copy()
        val=50
        if count>50:
            for i in range(val):  
                if count % val==i:
                    print(f"analysing image {i}")
                    fname = "./img_analysis/june23_withlargemag_right.npz"
                    IMAGE_LIST.append(image_data)
                    np.savez(fname,*IMAGE_LIST)
                
            if len(IMAGE_LIST) == val:
                arr0 = np.zeros(CAM_IMG_SIZE)
                for arr in IMAGE_LIST:
                    arr0 += arr
                arr0 /= val
                #print(np.max(arr0))
                mean_arr = np.mean(arr0[arr0>1800])
                print(mean_arr)   
                arr0=np.zeros(CAM_IMG_SIZE)
                exit()
                    
        

        

image_queue = queue.Queue()

def image_to_bytes(image):
    buf = image.to_bytearray()[0]
    width, height = image.get_size()
    data = np.frombuffer(buf, dtype='<u2')   # uint16 little‐endian
    
    arr = data.reshape((height, width))
    return arr

def update_plot(*args):

    try:
        while True:  # Drain the queue
            image_data = image_queue.get_nowait()
            
            original_image.set_clim(vmin=np.min(image_data), vmax=np.max(image_data))
            original_image.set_data(image_data)
            
            # image_transformed = ff.apply_transformations(image_data)
            image_transformed = image_data - MAG_BASELINE
            filtered_image.set_clim(vmin=np.min(image_transformed), vmax=np.max(image_transformed))
            filtered_image.set_data(image_transformed)
            
            print("updating plot")
            fig.canvas.draw_idle()
            fig.canvas.flush_events()
            
            # save

            

    except queue.Empty:
        pass
    fig.canvas.flush_events()
    # Return True to keep the timer running
    return True

def main():
    global original_image, filtered_image, fig
    
    
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    data = np.zeros(CAM_IMG_SIZE)
    

    original_image = ax[0].imshow(data, cmap='gray')  # Assuming 16-bit grayscale
    ax[0].set_title("Original Image")
    ax[0].axis('off')
    filtered_image = ax[1].imshow(MAG_BASELINE, cmap='gray')
    ax[1].set_title("After Filters")
    ax[1].axis('off')
    plt.ion()  # Interactive mode ON



    cam = MyThorCam()
    cam.start_cam_process()
    # cam.refresh_cameras()
    
    cam.open_camera("29035")
    
    cam.set_setting('exposure_ms', 1)
    cam.set_setting('trigger_type', 'SW Trigger')
    cam.set_setting('trigger_count', 2000)

    
    # print(cam.exposure_range)
    
    cam.play_camera()
    
    
    print("start timer")
    timer = fig.canvas.new_timer(interval=100)
    timer.add_callback(update_plot)
    timer.start()


    plt.show(block=True)  # Show the plot without blocking
    
    cam.close_camera()
    cam.stop_cam_process(join=True)
    exit()


if __name__ == "__main__":
    main()
