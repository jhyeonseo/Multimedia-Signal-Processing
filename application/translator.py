import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
from scipy import signal
import numpy as np
import pyaudio
from scipy.io import wavfile
import googletrans
import keyboard
import wave
import os


RATE = 16000
CHUNK = 1600
p=pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,frames_per_buffer=CHUNK, input_device_index=0)
stream_OUT = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True)
r=sr.Recognizer()
translator = googletrans.Translator()

src = input("Input language: ")
dst = input("Output language: ")
os.system('cls' if os.name == 'nt' else 'clear')
while True:
    flag = None
    print("------------system menu------------")
    print("s: speaking")
    print("t: typing")
    print("q: quit system")
    while True:
        if keyboard.is_pressed('s'):
            flag = 's'
            break
        elif keyboard.is_pressed('t'):
            flag = 't'
            break
        elif keyboard.is_pressed('q'):
            flag = 'q'
            break
    if flag == 'q':
        break
    
    elif flag == 's':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Press 'e' to end speaking")
        stream.start_stream()
        speech = stream.read(CHUNK)
        data = np.frombuffer(speech, dtype=np.int16)
        while True:
            speech = stream.read(CHUNK)
            speech = np.frombuffer(speech, dtype=np.int16)
            data = np.concatenate([data,speech])
            if keyboard.is_pressed('e'):
                break
        stream.stop_stream()
        
        print("start translating")
        wavfile.write('temp.wav', RATE, data.astype(np.int16))
        wavr = sr.AudioFile('temp.wav')
        with wavr as source:
            audio = r.record(source)
            text = r.recognize_google(audio, language=src)
            
    elif flag == 't':
        os.system('cls' if os.name == 'nt' else 'clear')
        text = input("Enter string: ")
        print("start translating")
    
    translated_text = translator.translate(text, dest=dst).text
    os.system('cls' if os.name == 'nt' else 'clear')
    print("------------result------------")
    print("Input:", text)
    print("Translated:", translated_text)
    tts = gTTS(text=translated_text, lang=dst)
    tts.save('voice.wav')
    d, fs = sf.read('voice.wav')
    ds = signal.resample(d, int(len(d)*16/24))
    sf.write('voice.wav', ds, 16000)
    
    wf = wave.open("voice.wav", 'rb')
    data = wf.readframes(CHUNK)
    while data:
        stream_OUT.write(data)
        data = wf.readframes(CHUNK)
    
    print("")
    print("Press 'c' to continue...")
    while True:

        if keyboard.is_pressed('c'):
            os.system('cls' if os.name == 'nt' else 'clear')
            break

stream.stop_stream()
stream.close()
p.terminate()