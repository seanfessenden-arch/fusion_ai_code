import cv2
import time
from picamera2 import Picamera2
from camera_lesson22 import MyCamera
camera = MyCamera(640, 360, "Lesson 22")

topBar = 65
windowWaste = 25

cv2.namedWindow("Camera Small", cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow("Camera Small",  int(camera.WIDTH/2), int(camera.HEIGHT/2))
cv2.moveWindow("Camera Small",0,topBar+windowWaste+camera.HEIGHT)
    
cv2.namedWindow("Gray Small", cv2.WINDOW_GUI_NORMAL)
cv2.resizeWindow("Gray Small", int(camera.WIDTH/2), int(camera.HEIGHT/2))
cv2.moveWindow("Gray Small",int(camera.WIDTH/2),topBar+windowWaste+camera.HEIGHT)

def function_to_inject():
    frame= piCam.capture_array()
    camera.draw_fps(frame)
    
    print(frame[int(H/2),int(W/2)])
    frame[int(H/2):int(H/2)+10,int(W/2):int(W/2)+10] = [0,0,255]
    
    ROI = frame[int(H*.25):int(H*.75),int(W*.25):int(W*.75)].copy()

    ROI[int(.25*H*.5):int(.75*H*.5),int(.25*W*.5):int(.75*W*.5)] = [0,0,0]
    ROIgray = cv2.cvtColor(ROI,cv2.COLOR_BGR2GRAY) 
 
    frameSmall=cv2.resize(frame,(int(W/2),int(H/2)))
    
    cv2.imshow(MyCamera.video, frame)
    cv2.imshow("Camera Small",ROI)
    cv2.imshow("Gray Small",ROIgray)
    
camera.injected_function(function_to_inject)