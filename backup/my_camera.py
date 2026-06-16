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
        
        self.fps = 0
        
        self.display_text = "Text to display"
        
        self.bouncing_box = BouncingBox(30, 40, dx=7, dy=7)
        
        self.detections = [{
            "label": "Person",
            "conf": 97,
            "x": 250,
            "y": 150,
            "w": 200,
            "h": 300
        },
        {
            "label": "Dog",
            "conf": 89,
            "x": 700,
            "y": 250,
            "w": 180,
            "h": 150
        }]
        
        RES = (width, height)
        
        self.running = True
        
        self.piCam.preview_configuration.main.size = RES
        self.piCam.preview_configuration.main.format = 'RGB888'
        self.piCam.preview_configuration.align()
        self.piCam.preview_configuration.controls.FrameRate = 60
        self.piCam.configure('preview')
        self.piCam.start()

    def capture_picture(self):
        frame = self.piCam.capture_array()
        cv2.imshow(MyCamera.picture, frame)
        cv2.moveWindow(MyCamera.picture, 0, 60)
        if cv2.waitKey(0) == ord('q'):
            cv2.destroyAllWindows()
    #end capture_picture
            
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
            
            self.draw_fps(frame)
            
            match self.overlay:
                case MyCamera.BOX:
                    self.draw_box(frame)
                case MyCamera.TRIANGLE:
                    self.draw_triangle(frame)
                case MyCamera.TEXT:
                    self.draw_text(frame)
                case MyCamera.CROSSHAIR:
                    self.draw_crosshair(frame)
                case MyCamera.DETECTION:
                    self.draw_detections(frame)
                case MyCamera.BOUNCE:
                    self.draw_bouncing_box(frame)
                case _:
                    pass
            cv2.imshow(MyCamera.video, frame)
            
            if cv2.waitKey(1) == ord('q'): #need the '1' so that the loop will work
                break
        cv2.destroyAllWindows()
    #end capture_video
        
    def draw_box(self, frame):
        upperLeft = (int((self.WIDTH-1)*0.1), int((self.HEIGHT-1)*0.1))

        lowerRight = (int((self.WIDTH-1)*0.9),int((self.HEIGHT-1)*0.9))

        cv2.rectangle(frame, upperLeft, lowerRight, (255,0,0), int(self.WIDTH/250))
    #end draw_box
        
    def draw_triangle(self, frame):
        pts = np.array([
            [self.WIDTH // 2, self.HEIGHT // 5],
            [self.WIDTH // 5, self.HEIGHT * 4 // 5],
            [self.WIDTH * 4 // 5, self.HEIGHT * 4 // 5]
        ])

        cv2.polylines(
            frame,
            [pts],
            True,
            (0, 255, 0),
            3
        )
    #end draw_triangle

    def draw_fps(self, frame):
        #cv2.putText(img, text, org, fontFace, fontScale, color, thickness, lineType, bottomLeftOrigin)
        cv2.putText(frame,f"FPS: {self.fps:.1f}",(5, self.HEIGHT-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255, 255, 255),1)
    #end draw_fps

    def draw_text(self, frame):
        cv2.putText(
            frame,
            self.display_text,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 255),
            2
        )
    #end draw_text
        
    def set_text(self, disp_text):
        self.display_text = disp_text
        
    def draw_crosshair(self, frame):
        cx = self.WIDTH // 2
        cy = self.HEIGHT // 2

        cv2.line(frame, (cx, 0), (cx, self.HEIGHT), (0, 0, 255), 2)
        cv2.line(frame, (0, cy), (self.WIDTH, cy), (0, 0, 255), 2)
    #end draw_crosshair
        
    def draw_detections(self, frame):
        for det in self.detections:
            x = det["x"]
            y = det["y"]
            w = det["w"]
            h = det["h"]

            cv2.rectangle(frame,(x, y), (x + w, y + h),(0, 255, 0), 2)
            label = f'{det["label"]} {det["conf"]}%'
            cv2.putText(frame,label, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0, 255, 0),2 )
    #end draw_detections
            
    def draw_bouncing_box(self, frame):
        frame_h, frame_w = frame.shape[:2]
        self.bouncing_box.update(frame_w, frame_h)
        #print(self.bouncing_box)
        self.bouncing_box.draw(frame)
        
        
    def stop(self):
        self.running = False
        cv2.destroyAllWindows()
        print("Exiting program")
        
if __name__ == "__main__":
    myCam = MyCamera(640, 480, "Test MyCamera")

    videoThread = th.Thread(target=myCam.capture_video, daemon = False)
    videoThread.start()
    myCam.overlay = MyCamera.BOX
    sleep(3)
    
    myCam.overlay = MyCamera.TRIANGLE
    sleep(3)
    
    myCam.overlay = MyCamera.CROSSHAIR
    sleep(3)

    myCam.overlay = MyCamera.TEXT
    sleep(3)
    
    myCam.overlay = MyCamera.DETECTION
    myCam.detections = [
        {
            "label": "Person",
            "conf": 97,
            "x": 250,
            "y": 150,
            "w": 200,
            "h": 300
        },
        {
            "label": "Dog",
            "conf": 89,
            "x": 700,
            "y": 250,
            "w": 180,
            "h": 150
        }
    ]
    sleep(3)
    
    myCam.overlay = MyCamera.BOUNCE
    sleep(3)

    myCam.overlay = MyCamera.NONE
    myCam.stop()
    videoThread.join()
