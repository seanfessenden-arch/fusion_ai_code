from my_camera import MyCamera
from bouncing_box import BouncingBox
from fusion_hat.stt import STT
from fusion_hat.tts import Piper
import time
import threading as th
import cv2

quit_event = th.Event()
stt = STT(language="en-us")
tts = Piper()
tts.set_model('en_US-kristin-medium')

win_Width = 1280
win_Height = 720

if __name__ == "__main__":
    myCam = MyCamera(win_Width, win_Height, "Bouncing Box")
    t = th.Thread(target=myCam.capture_video, daemon=False)
    print("Waiting for thread to start ...")
    t.start()
    
    tts.say("Say QUIT to end program")

    try:
        while not quit_event.is_set():
            cmd = stt.listen(stream=False)
            print(f"cmd = {cmd}")
            match cmd:
                case "quit":
                    myCam.stop()
                    quit_event.set()
                case "bounce":
                    myCam.overlay = MyCamera.BOUNCE
        t.join()
        print("Exiting program ...")
    except KeyboardInterrupt:
        quit_event.set()
        print("Exiting program ...")