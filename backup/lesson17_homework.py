from my_camera import MyCamera
from fusion_hat.stt import STT
from fusion_hat.tts import Piper
from fusion_hat.servo import Servo   # Import the Servo class for controlling servos
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
    myCam = MyCamera(win_Width, win_Height, "Test Picture")
    t = th.Thread(target=myCam.capture_video, daemon=False)
    print("Waiting for thread to start ...")
    t.start()
    
    tts.say("Say a Key word. They are: box, text, triangle, cross hair, detect or QUIT")

    try:
        while not quit_event.is_set():
            cmd = stt.listen(stream=False)
            print(f"cmd = {cmd}")
            match cmd:
                case "quit":
                    myCam.stop()
                    quit_event.set()
                case "box":
                    myCam.overlay = MyCamera.BOX
                case "triangle":
                    myCam.overlay = MyCamera.TRIANGLE
                case "cross hair" | "cross here":
                    myCam.overlay = MyCamera.CROSSHAIR
                case "text":
                    myCam.set_text("Display this text")
                    myCam.overlay = MyCamera.TEXT
                case "detect":
                    myCam.overlay = MyCamera.DETECTION
        t.join()
        print("Exited program")
    except KeyboardInterrupt:
        quit_event.set()
        print("Exit")