#!/bin/python
import threading as th
from queue import Queue as QU
from time import sleep
from fusion_hat import *

colorQ = QU()
quit_event = th.Event()
stt = STT()
tts = TTS("en-us")
redPin = 5
greenPin = 6
bluePin = 7

redLED = Pin(redPin, mode=Mode.OUT)
greenLED = Pin(greenPin, mode=Mode.OUT)
blueLED = Pin(bluePin, mode=Mode.OUT)

def runme():
    i =0
    while not quit_event.is_set():
        tts.speak("What color would you like the LED, or off")
        cmd = stt.listen(stream=False) 

        match cmd.strip():
            case "off":
                quit_event.set()
                redLED.low()
                greenLED.low()
                blueLED.low()
                print("Exit")
                break
            case "red"|"green"|"blue"|"magenta"|"cyan" |"yellow":
                colorQ.put(cmd)
#end runme

if __name__ == "__main__":
    run = th.Thread(target=runme)
    run.start()
    try:
        while not quit_event.is_set():
            if not colorQ.empty():
                cmd = colorQ.get()
                match cmd:
                    case "red":
                        redLED.high()
                    case "green":
                        greenLED.high()
                    case "blue":
                        blueLED.high()
                    case "magenta":
                        redLED.high()
                        blueLED.high()
                    case "cyan":
                        greenLED.high()
                        blueLED.high()
                    case "yellow":
                        redLED.high()
                        greenLED.high()
    except KeyboardInterrupt:
        redLED.low()
        greenLED.low()
        blueLED.low()
        print("Exit")
    run.join()

