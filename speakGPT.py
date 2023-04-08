import speech_recognition as sr
from gtts import gTTS
import soundfile as sf
from scipy import signal
import numpy as np
import pyaudio
from scipy.io import wavfile
import keyboard
import wave
import os
import openai

RATE = 16000
CHUNK = 1600
p=pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,frames_per_buffer=CHUNK, input_device_index=0)
stream_OUT = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True)
r=sr.Recognizer()

openai.api_key = "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"
prompt = []
src = input("Type your language: ")
os.system('cls' if os.name == 'nt' else 'clear')
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Press 's' to start speaking")
    print("Press 'q' to quit")
    flag = None
    while True:
        if keyboard.is_pressed("s"):
            break 
        if keyboard.is_pressed("q"):
            flag = 'q'
            break 
    if flag == 'q':
        break
    
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
            print("Waiting AI")
            break
    stream.stop_stream()
    wavfile.write('temp.wav', RATE, data.astype(np.int16))
    wavr = sr.AudioFile('temp.wav')
    with wavr as source:
        audio = r.record(source)
        text = r.recognize_google(audio, language=src)
    
    
    message  = {'role': 'user', 'content': text + "#짧은 답변"}
    prompt.append(message)
    response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = prompt,
    max_tokens = 128,
    temperature = 0.7,
    )
    ai_response = response['choices'][0]['message']['content']
    message = {'role': 'assistant', 'content': ai_response}
    prompt.append(message)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Input:", text)
    print("Received:", ai_response)
    tts = gTTS(text=ai_response, lang=src)
    tts.save('voice.wav')
    d, fs = sf.read('voice.wav')
    ds = signal.resample(d, int(len(d)*16/24))
    sf.write('voice.wav', ds, 16000)
    
    wf = wave.open("voice.wav", 'rb')
    data = wf.readframes(CHUNK)
    while data:
        stream_OUT.write(data)
        data = wf.readframes(CHUNK)

os.system('cls' if os.name == 'nt' else 'clear')

file_path = "prompt.txt"


with open(file_path, "w") as file:
    for data in prompt:
        line = data['role'] + ": " + data['content'].split('#')[0]
        file.write(line+'\n')

stream.stop_stream()
stream.close()
p.terminate()