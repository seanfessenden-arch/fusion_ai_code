import cv2
from time import time, perf_counter
from picamera2 import Picamera2
piCam = Picamera2()
#W=1280
#H=720
win_name = "Camera"

W = 640
H = 480
tStart = time()
fps = 0
RES = (W,H)
piCam.preview_configuration.main.size = RES
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.controls.FrameRate=60
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

textLowerLeft = (int(W*.01),int(H*.05))
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontThickness = int(W/425)
fontScale = H*.0015
fontColor = (0,0,255)

cv2.namedWindow(win_name)
cv2.moveWindow(win_name,0,60)

while True:
    deltaT = time() - tStart
    tStart=time()
    fps = fps*.95 + (1/deltaT)*.05
    
#     t0 = perf_counter()
    frame = piCam.capture_array()
#     capture_ms = (perf_counter() - t0) * 1000
#     print(f"Capture: {capture_ms:.1f} ms")
    
    #frame=cv2.flip(frame,-1)
    myText = "FPS: "+str(round(fps,1))
    cv2.putText(frame,myText,textLowerLeft,fontFace,fontScale,fontColor,fontThickness)
    cv2.imshow(win_name, frame)
    #cv2.moveWindow("Camera",0,60)
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()
print('Program Terminated')