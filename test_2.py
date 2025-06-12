from thorcam.camera import ThorCam
import time
class MyThorCam(ThorCam):
    def received_camera_response(self, msg, value):
        super(MyThorCam, self).received_camera_response(msg, value)
        if msg == 'image':
            return
        print('Received "{}" with value "{}"'.format(msg, value))
    def got_image(self, image, count, queued_count, t):
        print('Received image "{}" with time "{}" and counts "{}", "{}"'
              .format(image, t, count, queued_count))

def main():
    cam = MyThorCam()
    cam.start_cam_process()
    # cam.refresh_cameras()
    
    cam.open_camera("29035")
    
    # print(cam.exposure_range)
    cam.play_camera()
    
    # cam.close_camera()
    print("will sleep 2 s")
    time.sleep(2.8)
    
    
    
    cam.close_camera()
    cam.stop_cam_process(join=True)
    exit()


if __name__ == "__main__":
    main()
