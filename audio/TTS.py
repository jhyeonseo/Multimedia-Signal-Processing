import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
from scipy import signal
import playsound
s=input("Enter string: ")
tts = gTTS(text=s, lang='en')
tts.save('voice.wav')
d, fs = sf.read('voice.wav')
ds = signal.resample(d, int(len(d)*16/24))
sf.write('voice.wav', ds, 16000)
playsound.playsound('voice.wav')