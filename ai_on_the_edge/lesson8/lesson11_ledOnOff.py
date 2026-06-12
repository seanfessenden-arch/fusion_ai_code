from fusion_hat.stt import STT
from fusion_hat.pin import Pin, Mode
from time import sleep

redPin = 17
redLED = Pin(redPin,mode=Mode.OUT)
stt = STT(language="en-us")

try:
    while True:
        print("Speak command, ON or OFF: ")
        command = stt.listen(stream=False)
        command = command.strip()
        print(f" LED {command}")
        if command == "on":
            redLED.high()
        if command == "off":
            redLED.low()
        if command == "quit":
            break
except KeyboardInterrupt:
    redLED.low()
    print("exit program")