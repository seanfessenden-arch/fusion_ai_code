#!/bin/python
from fusion_hat.pwm import PWM
import threading as th
from queue import Queue as QU
from time import sleep
from fusion_hat.stt import STT
from fusion_hat.tts import Piper

colorQ = QU()
quit_event = th.Event()
stt = STT(language="en-us")
tts = Piper()
tts.set_model('en_US-kristin-medium')

#LED Brightness is 100, 0 is off
ON = 100
OFF = 0

redPin = 5
greenPin = 6
bluePin = 7

redLED = PWM(redPin)
greenLED = PWM(greenPin)
blueLED = PWM(bluePin)

def runme():
    i =0
    while not quit_event.is_set():
        tts.say("What color would you like the LED, or off")
        cmd = stt.listen(stream=False) 
        print(f"cmd = {cmd}")
        
        match cmd.strip():
            case "off":
                quit_event.set()
                redLED.enable(False)
                greenLED.enable(False)
                blueLED.enable(False)
                print("Exit")
                break
            case "red" |"read"|"green"|"blue"|"magenta"|"cyan" |"yellow":
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
                    case "red" | "read":
                        redLED.pulse_width_percent(ON)
                        blueLED.pulse_width_percent(OFF)
                        greenLED.pulse_width_percent(OFF)
                    case "green":
                        greenLED.pulse_width_percent(ON)
                        redLED.pulse_width_percent(OFF)
                        blueLED.pulse_width_percent(OFF)
                    case "blue":
                        blueLED.pulse_width_percent(ON)
                        greenLED.pulse_width_percent(OFF)
                        redLED.pulse_width_percent(OFF)
                    case "magenta":
                        redLED.pulse_width_percent(ON)
                        blueLED.pulse_width_percent(ON)
                        greenLED.pulse_width_percent(OFF)
                    case "cyan":
                        greenLED.pulse_width_percent(ON)
                        blueLED.pulse_width_percent(ON)
                        redLED.pulse_width_percent(OFF)
                    case "yellow":
                        redLED.pulse_width_percent(ON)
                        greenLED.pulse_width_percent(ON)
                        blueLED.pulse_width_percent(OFF)
    except KeyboardInterrupt:
        redLED.enable(False)
        greenLED.enable(False)
        blueLED.enable(False)
        print("Exit")
    run.join()

