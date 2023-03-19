import numpy as np
import pyaudio
import keyboard
import audio
import options
import wave

options = options.AudioOptions()
opts = options.parse()
print(vars(opts))
p=pyaudio.PyAudio()

if opts.mode == "realtime":
    audio = audio.AudioManager(opts)
    stream = p.open(format=opts.format, 
                    channels=opts.channels, 
                    rate=opts.rate, 
                    input=True, 
                    output=True, 
                    frames_per_buffer=opts.chunk, 
                    input_device_index=opts.device)
    print("Real time mode")
    while(True):
        samples = stream.read(opts.chunk)
        out = audio.process(samples)
        stream.write(out)
        if keyboard.is_pressed('c'):
            audio.change()
        elif keyboard.is_pressed('q'):
            break
        
elif opts.mode == "record":
    audio = audio.AudioManager(opts)
    stream = p.open(format=opts.format, 
                    channels=opts.channels, 
                    rate=opts.rate, input=True, 
                    output=True, 
                    frames_per_buffer=opts.chunk, 
                    input_device_index=opts.device)
    print("Record mode")
    audio.change()
    frames = []
    while(True):
        samples = stream.read(opts.chunk)
        out = audio.process(samples)
        frames.append(out)
        if keyboard.is_pressed('q'):
            break
    wf = wave.open("audio.wav", 'wb')
    wf.setnchannels(opts.channels)
    wf.setsampwidth(p.get_sample_size(opts.format))
    wf.setframerate(opts.rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
elif opts.mode == "play":
    wf = wave.open("audio.wav", 'rb')
    opts.format = p.get_format_from_width(wf.getsampwidth())
    opts.channels = wf.getnchannels()
    opts.rate = rate=wf.getframerate()
    audio = audio.AudioManager(opts)
    stream = p.open(format=opts.format,
                 channels=opts.channels,
                 rate=opts.rate,
                 output=True)
    print("Play mode")
    audio.change()
    data = wf.readframes(1024)
    frames = []
    while data:
        data = audio.process(data)
        stream.write(data)
        frames.append(data)
        data = wf.readframes(1024)
        if keyboard.is_pressed('q'):
            break
    wf = wave.open("transformed.wav", 'wb')
    wf.setnchannels(opts.channels)
    wf.setsampwidth(p.get_sample_size(opts.format))
    wf.setframerate(opts.rate)
    wf.writeframes(b''.join(frames))
    wf.close()
        
        
stream.stop_stream()
stream.close()
p.terminate()

