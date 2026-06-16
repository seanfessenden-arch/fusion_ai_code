import cv2
from picamera2 import Picamera2
from bouncing_box import BouncingBox
from time import sleep, perf_counter
import threading as th
import numpy as np

class MyCamera:
    picture = "Picture"
    video = "Video"
    NONE = 0
    BOX = 1
    TRIANGLE = 2
    TEXT = 3
    CROSSHAIR = 4
    DETECTION = 5
    BOUNCE = 6
    
    def __init__(self, width, height, frame_name):
        
        self.piCam = Picamera2()
        
        self.WIDTH = width
        self.HEIGHT = height
        
        self.overlay = MyCamera.NONE
        
        self.bouncing_box = BouncingBox(10, 10, 30, 30, dx=5, dy=5)
        
        RES = (width, height)
        
        self.running = True
        
        self.piCam.preview_configuration.main.size = RES
        self.piCam.preview_configuration.main.format = 'RGB888'
        self.piCam.preview_configuration.align()
        self.piCam.preview_configuration.controls.FrameRate = 60
        self.piCam.configure('preview')
        self.piCam.start()
            
    def capture_video(self):
        cv2.namedWindow(MyCamera.video)
        cv2.moveWindow(MyCamera.video, 0, 60)
        
        frame_count = 0
        start_time = perf_counter()
        fps = 0
    
        while self.running:
            frame = self.piCam.capture_array()
            
            #Track the FPS, count the frames, then if more than 1 sec has passed, divide
            #the number of frames by the elapsed time to get FPS
            frame_count += 1
            elapsed = perf_counter() - start_time
            if elapsed >= 1.0:
                self.fps = frame_count / elapsed
                frame_count = 0
                start_time = perf_counter()
            
            match self.overlay:
                case MyCamera.BOUNCE:
                    self.draw_bouncing_box(frame)
                case _:
                    pass
            cv2.imshow(MyCamera.video, frame)
            
            if cv2.waitKey(1) == ord('q'): #need the '1' so that the loop will work
                break
        cv2.destroyAllWindows()
    #end capture_video

            
    def draw_bouncing_box(self, frame):
        frame_h, frame_w = frame.shape[:2]
        self.bouncing_box.update(frame_w, frame_h)
        self.bouncing_box.draw(frame)
        
        
    def stop(self):
        self.running = False
        cv2.destroyAllWindows()
        print("Exiting program")
        
if __name__ == "__main__":
    myCam = MyCamera(640, 480, "Test MyCamera")

    videoThread = th.Thread(target=myCam.capture_video, daemon = False)
    videoThread.start()

    myCam.overlay = MyCamera.BOUNCE
    sleep(20)

    myCam.overlay = MyCamera.NONE
    myCam.stop()
    videoThread.join()

