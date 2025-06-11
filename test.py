# import time
#import cv2
# import numpy as np
# from thorcam import camera

# camera.ThorCamClient.thor_bin_path = r"C:\Program Files\Thorlabs\Scientific Imaging\ThorCam"

from thorcam.camera import ThorCam
from thorcam.camera import ThorCamClient


# class MyThorCam(ThorCam):
#     def received_camera_response(self, msg, value):
#         super(MyThorCam, self).received_camera_response(msg, value)
#         if msg == 'image':
#             return
#         print('Received "{}" with value "{}"'.format(msg, value))
#     def got_image(self, image, count, queued_count, t):
#         print('Received image "{}" with time "{}" and counts "{}", "{}"'
#               .format(image, t, count, queued_count))







def main():
    ThorCamClient.thor_bin_path=r"C:\Program Files\Thorlabs\Scientific Imaging\ThorCam"

    cam = ThorCam()
    cam.start_cam_process()
    cam.refresh_cameras()
    # print(cam.received_camera_response(msg, value))
    
    
    #print(cam.refresh_cameras())
# def main():
#     # Connect to the first available camera
#     cam = camera.ThorlabsCamera()
#     cam.open()

#     # Start acquisition
#     cam.start_video_capture()

#     print("Press 'q' in the video window to quit.")

#     try:
#         while True:
#             frame = cam.get_pending_frame(timeout_ms=1000)

#             if frame is not None:
#                 image = frame.image_buffer
#                 # Convert to uint8 image (OpenCV expects 8-bit)
#                 image = np.array(image, dtype=np.uint8)

#                 # Display the image using OpenCV
#                 cv2.imshow("Live - CS505MU1", image)

#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     break

#     except KeyboardInterrupt:
#         print("Interrupted by user.")
#     finally:
#         # Clean up
#         cam.stop_video_capture()
#         cam.close()
#         cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
