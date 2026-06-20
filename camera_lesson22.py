import cv2
from picamera2 import Picamera2
from bouncing_box import BouncingBox
from time import sleep, perf_counter
import threading as th
import numpy as np

class MyCamera:
    video = "Video"
    NONE = 0
    FUNCTION = 1
    
    def __init__(self, width, height, frame_name):
        
        self.piCam = Picamera2()
        
        self.WIDTH = width
        self.HEIGHT = height
        
        self.overlay = MyCamera.NONE
        
        self.fps = 0
        self.function = False 
        
        RES = (width, height)
        
        self.running = True
        
        self.piCam.preview_configuration.main.size = RES
        self.piCam.preview_configuration.main.format = 'RGB888'
        self.piCam.preview_configuration.align()
        self.piCam.preview_configuration.controls.FrameRate = 60
        self.piCam.configure('preview')
        self.piCam.start()
            
    def capture_video(self):
        top_bar =60
        bottom_bar = 25

        cv2.namedWindow(MyCamera.video, cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(MyCamera.video, self.WIDTH, self.HEIGHT)
        cv2.moveWindow(MyCamera.video,0,top_bar)
        
        #start setup of the Frames Per Second
        frame_count = 0
        start_time = perf_counter()
    
        while self.running:
            frame = self.piCam.capture_array()
            
            #the number of frames by the elapsed time to get FPS
            frame_count += 1
            elapsed = perf_counter() - start_time
            if elapsed >= 1.0:
                self.fps = frame_count / elapsed
                frame_count = 0
                start_time = perf_counter()
    
            
            
            self.draw_fps(frame)
            
            self.function()
            
            cv2.imshow(MyCamera.video, frame)
            
            if cv2.waitKey(1) == ord('q'): #need the '1' so that the loop will work
                break
        cv2.destroyAllWindows()
    #end capture_video
        
    def draw_fps(self, frame):
        cv2.putText(frame,f"FPS: {self.fps:.1f}",(5, self.HEIGHT-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255, 255, 255),1)
    #end draw_fps
       
    def stop(self):
        self.running = False
        cv2.destroyAllWindows()
        print("Exiting program")
        
    def injected_function(self, function):
        self.function = function
        
if __name__ == "__main__":
    myCam = MyCamera(640, 360, "Test MyCamera")

    videoThread = th.Thread(target=myCam.capture_video, daemon = False)
    videoThread.start()

    myCam.overlay = MyCamera.FUNCTION
    sleep(5)

    myCam.overlay = MyCamera.NONE
    myCam.stop()
    videoThread.join()
