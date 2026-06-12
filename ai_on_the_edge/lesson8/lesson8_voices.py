from fusion_hat.tts import Piper

tts = Piper()
tts.set_model('en_US-amy-low')
msg = "Test this voice"
tts.say(msg, stream=False)