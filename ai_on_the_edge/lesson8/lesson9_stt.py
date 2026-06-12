from fusion_hat.stt import STT

stt  = STT(language='en-us')

while True:
    
    print("say something:")
    
    command = stt.listen(stream=False)
    print(command)

