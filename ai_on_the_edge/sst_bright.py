#!/bin/python
import threading as th
from queue import Queue as QU
from time import sleep
from fusion_hat import *

bNumb = 0
brightQ = QU()
quit_event = th.Event()
sst = SST()
redPin = 5
redLED = PWM(redPin)

def runme():
    i =0
    while not quit_event.is_set():
        print("What brightness(off, low, medium, high, on or quit")
        cmd = sst.listen(stream=False) 
        #cmd = input()
        if cmd.strip() == "quit":
            quit_event.set()
        match cmd:
            case "quit":
                quit_event.set()
                break
            case "off"|"low"|"medium"|"high"|"on":
                brightQ.put(cmd)
        #print(f"**brightQ={brightQ.get()}")
#end runme

if __name__ == "__main__":
    run = th.Thread(target=runme)
    run.start()
    try:
        while not quit_event.is_set():
            if not brightQ.empty():
                cmd = brightQ.get()
                match cmd:
                    case "off":
                        bNumb = 0
                    case "low":
                        bNumb = 8
                    case "medium":
                        bNumb = 25
                    case "high":
                        bNumb = 60
                    case "on":
                        bNumb = 100
                print("not empty")
                redLED.pulse_width_percent(bNumb)
                #break

           # redLED.pulse_width_percent(bNumb)
           # redLED.enable(False)
    except KeyboardInterrupt:
       # redLed.pulse_width_percent(0)
       # redLed.enable(False)
        print("Exit")
    run.join()

