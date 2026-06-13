import cv2
from picamera2 import Picamera2

class MyCamera:
    picture = "Picture"
    video = "Video"
    
    def __init__(self, width, height, frame_name):
        self.piCam = Picamera2()
        self.WIDTH = width
        self.HEIGHT = height
        RES = (width, height)
        self.piCam.preview_configuration.main.size = RES
        self.piCam.preview_configuration.main.format = 'RGB888'
        self.piCam.preview_configuration.align()
        self.piCam.configure('preview')
        self.piCam.start()

    def capture_picture(self):
        frame = self.piCam.capture_array()
        cv2.imshow(MyCamera.picture, frame)
        cv2.moveWindow(MyCamera.picture, 0, 60)
        if cv2.waitKey(0) == ord('q'):
            cv2.destroyAllWindows()
            
    def capture_video(self):
        while True:
            frame = self.piCam.capture_array()
            cv2.imshow(MyCamera.video, frame)
            cv2.moveWindow(MyCamera.video, 0, 60)
            if cv2.waitKey(1) == ord('q'): #need the '1' so that the loop will work
                cv2.destroyAllWindows()
        
if __name__ == "__main__":
    myCam = MyCamera(1280, 720, "Test Picture")
    myCam.capture_picture()
    myCam.capture_video()