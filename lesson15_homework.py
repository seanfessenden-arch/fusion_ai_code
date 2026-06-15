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
panPin=2
tiltPin=3
servoPan = Servo(panPin)
servoTilt=Servo(tiltPin)


if __name__ == "__main__":
    myCam = MyCamera(1280, 720, "Test Picture")
    t = th.Thread(target=myCam.capture_video)
    t.start()
    
    pan_angle = 0
    tilt_angle = 0
    servoPan.angle(pan_angle)
    servoTilt.angle(tilt_angle)

    tts.say("Move the camera around, say Up, Down, Left, Right or Quit")

    try:
        while not quit_event.is_set():
            cmd = stt.listen(stream=False)
            print(f"cmd = {cmd}")
            match cmd:
                case "quit":
                    myCam.stop()
                    quit_event.set()
                case "up":
                    tilt_angle = tilt_angle - 10
                    servoTilt.angle(tilt_angle)
                case "down":
                    tilt_angle = tilt_angle + 10
                    servoTilt.angle(tilt_angle)
                case "left":
                    pan_angle = pan_angle + 10
                    servoPan.angle(pan_angle)
                case "right":
                    pan_angle = pan_angle - 10
                    servoPan.angle(pan_angle)

        t.join()
    except KeyboardInterrupt:
        quit_event.set()
        print("Exit")