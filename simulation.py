from utils.CAMERA_SIM import CAMERA_SIM
import time
import numpy as np
import utils.functions_file as ff

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import queue


# camera image size
CAM_IMG_SIZE = (2448, 2048)  # CS505MU1

image_queue = queue.Queue()

def image_to_bytes(image):
    buf = image.to_bytearray()[0]
    width, height = image.get_size()
    data = np.frombuffer(buf, dtype='<u2')   # uint16 little‐endian
    arr = data.reshape((height, width))

    NOISE_INTENITY = 0.7 * np.max(arr)  # 20% of max value
    noise  = np.random.randint(-NOISE_INTENITY, NOISE_INTENITY, size=arr.shape)
    noisy_data = arr + noise
    return noisy_data 


def got_image(image, count): # does not use queued_count or t
    image_data = image_to_bytes(image)
    image_queue.put(image_data)


def update_plot(*args):
    try:
        while True:  # Drain the queue
            image_data = image_queue.get_nowait()
            
            original_image.set_clim(vmin=np.min(image_data), vmax=np.max(image_data))
            original_image.set_data(image_data)

            image_transformed = ff.apply_transformations(image_data)
            filtered_image.set_clim(vmin=np.min(image_transformed), vmax=np.max(image_transformed))
            filtered_image.set_data(image_transformed)

            print("updating plot")
            fig.canvas.draw_idle()
            fig.canvas.flush_events()

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
    filtered_image = ax[1].imshow(data, cmap='gray')
    ax[1].set_title("After Filters")
    ax[1].axis('off')
    plt.ion()  # Interactive mode ON



    cam = CAMERA_SIM()
    cam.start_cam_process()
    # cam.refresh_cameras()
    cam.got_image = got_image
    
    cam.open_camera("29035")
    
    # print(cam.exposure_range)
    
    cam.play_camera()

    timer = fig.canvas.new_timer(interval=100)
    timer.add_callback(update_plot)
    timer.start()


    plt.show(block=True)  # Show the plot without blocking
    
    cam.close_camera()
    cam.stop_cam_process(join=True)
    exit()




if __name__ == "__main__":
    main()