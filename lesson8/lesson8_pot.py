#!/usr/bin/env python3
from fusion_hat.adc import ADC
from fusion_hat.pwm import PWM
from time import sleep
from fusion_hat.tts import Piper

def map_range(value, in_min, in_max, out_min, out_max):
    x1 = (value - in_min)
    x2 = (out_max - out_min)
    x3 = (in_max - in_min)
    return (x1 * x2)  / x3  + out_min
#end map_range

tts = Piper()
tts.set_model('en_US-amy-low')

potPin=0
myPot = ADC(0)
redPin=5
redLED=PWM(redPin)

lastMapped = 100
while True:
    potVal = myPot.read() # 0 to 4095
    LEDPercent = int(map_range(potVal, 0, 4095, 0, 101))
    mappedVal = int(map_range(potVal, 0, 4095, 0, 11))
    redLED.pulse_width_percent(int(LEDPercent))
    print(f"LEDPercent = {LEDPercent}")
    
    if lastMapped != mappedVal:
        msg = f"LED is level {mappedVal}"
        tts.say(msg, stream=False)
        #print(f"lastVMapped= {lastMapped} and mappedVal = {mappedVal}")
        lastMapped = mappedVal
        
    sleep(0.1)
    