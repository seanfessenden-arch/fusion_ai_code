# import onnxruntime as ort
# ort.set_default_logger_severity(3)  # suppress warnings
# import onnxruntime as ort

# session = ort.InferenceSession(
#     "/opt/piper_models/en_US-amy-low.onnx",
#     providers=["CPUExecutionProvider"]
# )

from fusion_hat.tts import Piper

tts = Piper()
countries = tts.available_countrys()
for country in countries:
    print(f"country: {country}")
    
voiceDict = tts.available_models('en_US')
for voice in voiceDict:
    for speakableVoice in voiceDict[voice]:
        tts.set_model(speakableVoice)
        msg="my name is " + speakableVoice.replace('en_US-', '').replace('_', ' ').replace('-', ' ')
        print(msg)
        tts.say(msg, stream=False)
    
# tts.set_model('en_US-lessac-high')
# 
# msg = "Hi, I'm Piper TTS.  Are you ready to Rumble?  I am here to pump you up!"
# 
# tts.say(msg, stream=False)