
from thorcam.camera import ThorCam
from thorcam.camera import ThorCamClient


def main():
    ThorCamClient.thor_bin_path=r"C:\Program Files\Thorlabs\Scientific Imaging\ThorCam"

    cam = ThorCam()
    cam.start_cam_process()
    cam.refresh_cameras()
  

if __name__ == "__main__":
    main()
