#!/bin/python
"""
Dummy Fusion HAT classes for development/testing.
Replace with actual fusion_hat package on the Pi.
"""

#from enum import Enum


# ----------------------------------
# Mode
# ----------------------------------
#class Mode(Enum):
class Mode:
    IN = 0
    OUT = 1


# ----------------------------------
# Pin
# ----------------------------------
class Pin:
    HIGH = 1
    LOW = 0

    def __init__(self, pin_number, mode=Mode.OUT):
        self.pin_number = pin_number
        self.mode = mode
        self.state = Pin.LOW

    def write(self, value):
        self.state = value
        print(f"Pin {self.pin_number} -> {value}")

    def read(self):
        print(f"Reading Pin {self.pin_number}")
        return self.state

    def high(self):
        self.write(Pin.HIGH)

    def low(self):
        self.write(Pin.LOW)
# ----------------------------------
# PWM
# ----------------------------------
class PWM:
    def __init__(self, pin):
        self.pin = pin
        self.frequency = 1000
        self.duty_cycle = 0

    def freq(self, frequency):
        self.frequency = frequency
        print(f"PWM frequency = {frequency}")

    def pulse_width_percent(self, duty_cycle):
        self.duty_cycle = duty_cycle
        print(f"PWM duty = {duty_cycle}")


# ----------------------------------
# STT (Speech-to-Text)
# ----------------------------------
class STT:
    def __init__(self):
        print("Dummy STT initialized")

    def listen(self, stream=False):
        return input("Speak (type text): ")

    def start(self):
        print("Dummy STT started")

    def stop(self):
        print("Dummy STT stopped")


# ----------------------------------
# TTS (Text-to-Speech)
# ----------------------------------
class TTS:
    def __init__(self, str):
        print("Dummy TTS initialized")

    def say(self, text):
        print(f"TTS: {text}")

    def speak(self, text):
        print(f"TTS: {text}")


# ----------------------------------
# Example
# ----------------------------------
if __name__ == "__main__":

    led = Pin(17, Mode.OUT)

    led.write(Pin.HIGH)
    led.write(Pin.LOW)

    pwm = PWM(18)
    pwm.freq(1000)
    pwm.pulse_width_percent(50)

    stt = SST()
    text = stt.listen()

    tts = TTS()
    tts.say(f"You said: {text}")
