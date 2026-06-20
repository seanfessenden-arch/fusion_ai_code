import threading as th
import cv2
from base_camera import BaseCamera

#This pattern is often called the Template Method Pattern:
class Lesson22Camera(BaseCamera):
    
    cam_small = "Camera Small"
    cam_gray = "Camera Gray" 
    
    def initialize_windows(self):
        cv2.namedWindow(self.video, cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(self.video, self.WIDTH, self.HEIGHT)
        cv2.moveWindow(self.video, 0, self.top_bar)
        
        cv2.namedWindow(self.cam_small, cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(self.cam_small, int(self.WIDTH/2), int(self.HEIGHT/2))
        cv2.moveWindow(self.cam_small,0, self.top_bar + self.window_waste + self.HEIGHT)
            
        cv2.namedWindow(self.cam_gray, cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow(self.cam_gray, int(self.WIDTH/2), int(self.HEIGHT/2))
        cv2.moveWindow(self.cam_gray,int(self.WIDTH/2),self.top_bar + self.window_waste + self.HEIGHT)
 
    
    def process_frame(self, frame):
        #print(frame[int(self.WIDTH/2), int(self.HEIGHT/2)])
        frame[int(self.HEIGHT/2):int(self.HEIGHT/2)+10, int(self.WIDTH/2):int(self.WIDTH/2)+10] = [255,0,255]
    
        #Region Of Interest (ROI)
        self.ROI = frame[int(self.HEIGHT*.25):int(self.HEIGHT*.75),int(self.WIDTH*.25):int(self.WIDTH*.75)].copy()
        #change the ROI to black 
        self.ROI[int(.25*self.HEIGHT*.5):int(.75*self.HEIGHT*.5),int(.25*self.WIDTH*.5):int(.75*self.WIDTH*.5)] = [0,0,0]
        
        #Create another ROI that has a gray scale background
        self.ROIgray = cv2.cvtColor(self.ROI,cv2.COLOR_BGR2GRAY)
        
        #Need access to the frame, create a new object
        self.frame = frame
        
    def show_windows(self):
        cv2.imshow(self.video, self.frame)
        cv2.imshow(self.cam_small,self.ROI)
        cv2.imshow(self.cam_gray,self.ROIgray)

if __name__ == "__main__":
    myCam = Lesson22Camera(640, 360, "Lesson 22 Class")

    videoThread = th.Thread(target=myCam.capture_video, daemon = False)
    videoThread.start()
    videoThread.join()