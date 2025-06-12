# version 1.3
from thorcam.camera import ThorCam
import time
from PIL import Image

class MyThorCam(ThorCam):
    def received_camera_response(self, msg, value):
        super().received_camera_response(msg, value)
        # Print all non-image responses
        if msg != 'image':
            print(f'Received "{msg}" with value "{value}"')

    def got_image(self, image, count, queued_count, t):
        # Print and save the first received frame, then stop
        print(f'Received image "{image}" with time "{t}" and counts "{count}", "{queued_count}"')
        arr = image.to_ndarray()
        Image.fromarray(arr).save('snapshot.png')
        print('Saved snapshot.png')
        self.stop_playing_camera()


def main():
    cam = MyThorCam()
    cam.start_cam_process()

    # Discover and open the first camera
    cam.refresh_cameras()
    if not cam.serials:
        print('No cameras found!')
        return
    serial = cam.serials[0]
    print(f'Opening camera {serial}')
    cam.open_camera(serial)

    # Configure a single software-triggered snapshot
    cam.set_setting('exposure_ms', 100)
    cam.set_setting('trigger_type', 'SW Trigger')
    cam.set_setting('trigger_count', 1)

    # Start capture
    cam.play_camera()
    print('Waiting for image...')
    time.sleep(2)  # give time for the frame callback

    # Clean up
    cam.close_camera()
    cam.stop_cam_process(join=True)

if __name__ == '__main__':
    main()