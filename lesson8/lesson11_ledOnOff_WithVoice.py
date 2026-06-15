from fusion_hat.pin import Pin, Mode
import threading
from queue import Queue
from time import sleep

redPin = 17
redLED = Pin(redPin, Mode.OUT)
redLED.low()

blinkDelay = 1.0
blinkQ = Queue()
quit_event = threading.Event()

def blinkTime():
    print("blinkTime, thread start\n")
    while not quit_event.is_set():
        cmd = input("Input Blink Time in Seconds, or Q for Quit: ")
        if cmd.strip().lower()== "q":
            quit_event.set()
            break
        blinkQ.put(float(cmd))
    print("*** blinkTime, thread end\n")
#end blinkTime
    
blinkThread = threading.Thread(target=blinkTime,daemon=True)
blinkThread.start()
print("Main Program Started")

try:
    while not quit_event.is_set():
        if not blinkQ.empty():
            blinkDelay = blinkQ.get()
        redLED.high()
        sleep(blinkDelay)
        redLED.low()
        sleep(blinkDelay)
    redLED.low()
    print("Program Terminated")     
except KeyboardInterrupt:
    running = False
    redLED.low()
    print("LED Released")
    print("Program Terminated")