import cv2
import threading as th
from time import sleep, perf_counter
import numpy as np
from picamera2 import Picamera2

class BaseCamera:
    
    
    def __init__(self, width, height, frame_name):
        
        self.piCam = Picamera2()
        self.quit_event = th.Event()
        
        self.WIDTH = width
        self.HEIGHT = height
        
        self.video = frame_name
        
        self.top_bar = 60
        self.window_waste = 25
        self.fps = 0 
        
        self.piCam.preview_configuration.main.size = (width, height)
        self.piCam.preview_configuration.main.format = 'RGB888'
        self.piCam.preview_configuration.align()
        self.piCam.preview_configuration.controls.FrameRate = 60
        # 1. Apply the configuration to the camera pipeline
        self.piCam.configure('preview')
        # 2. Start the camera stream
        self.piCam.start()
        
    def process_frame(self, frame):
        """Override in child classes"""
        pass
    
    def initialize_windows(self):
        """Override in child classes"""
        pass
    
    def show_windows(self):
        """Override in child classes"""
        pass
    
    def capture_video(self):
        self.initialize_windows()

        frame_count = 0
        start_time = perf_counter()

        while not self.quit_event.is_set():

            frame = self.piCam.capture_array()

            # FPS calculation
            frame_count += 1
            elapsed = perf_counter() - start_time

            if elapsed >= 1.0:
                self.fps = frame_count / elapsed
                frame_count = 0
                start_time = perf_counter()

            # Child class hook
            self.process_frame(frame)

            # Common overlays
            self.draw_fps(frame)

            self.show_windows()

            if cv2.waitKey(1) == ord('q'):
                self.quit_event.set()

        cv2.destroyAllWindows()
        print("Exiting Program")
        
    def draw_fps(self, frame):
        cv2.putText(frame,f"FPS: {self.fps:.1f}",(5, self.HEIGHT-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255, 255, 255),1)
    #end draw_fps

