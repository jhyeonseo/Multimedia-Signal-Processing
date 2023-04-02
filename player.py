import numpy as np
import pyaudio
import keyboard
import audio
import options
import wave
import random

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
    print("____________Real time mode____________")
    while(True):
        samples = stream.read(opts.chunk)
        out = audio.process(samples,1,35)
        stream.write(out)
        if keyboard.is_pressed('c'):
            audio.change()
        elif keyboard.is_pressed('q'):
            break
    
elif opts.mode == "play":
    wf = wave.open("300hz.wav", 'rb')
    opts.format = p.get_format_from_width(wf.getsampwidth())
    opts.channels = wf.getnchannels()
    opts.rate = rate=wf.getframerate()
    audio = audio.AudioManager(opts)
    stream = p.open(format=opts.format,
                 channels=opts.channels,
                 rate=opts.rate,
                 output=True)
    print("____________Play mode____________")
   # audio.change()
    distance = 1
    angle = 90
    data = wf.readframes(opts.chunk)
    EFFECT = True
    while data:
        data = audio.process(data,distance,angle)
        stream.write(data)
        data = wf.readframes(opts.chunk)
        if keyboard.is_pressed('q'):
            break
        elif keyboard.is_pressed('s'):
            if EFFECT:
                EFFECT = False
                print("Sound effect off")
                keep_angle = angle
                keep_distance = distance
                angle = 0
                distance = 1
            else:
                EFFECT = True
                print("Sound effect on")
                angle = keep_angle
                distance = keep_distance
        else:
            if keyboard.is_pressed('a'):
                if angle > -180:
                    angle = angle - 2
                print("angle:",angle,"distance:",distance)
            elif keyboard.is_pressed('d'):
                if angle < 180:
                    angle = angle + 2
                print("angle:",angle,"distance:",distance)
            if keyboard.is_pressed('w'):
                if distance < 200:
                    distance = distance + 1
                print("angle:",angle,"distance:",distance)
            elif keyboard.is_pressed('s'):
                if distance > 0 :
                    distance = distance - 1
                print("angle:",angle,"distance:",distance)
        
elif opts.mode == "record":
    audio = audio.AudioManager(opts)
    stream = p.open(format=opts.format, 
                    channels=opts.channels, 
                    rate=opts.rate, input=True, 
                    output=True, 
                    frames_per_buffer=opts.chunk, 
                    input_device_index=opts.device)
    print("____________Record mode____________")
    audio.change()
    frames = []
    while(True):
        samples = stream.read(opts.chunk)
        out = audio.process(samples)
        frames.append(out)
        if keyboard.is_pressed('q'):
            break
    wf = wave.open("record.wav", 'wb')
    wf.setnchannels(opts.channels)
    wf.setsampwidth(p.get_sample_size(opts.format))
    wf.setframerate(opts.rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
elif opts.mode == "game":
    wf = wave.open("300hz.wav", 'rb')
    opts.format = p.get_format_from_width(wf.getsampwidth())
    opts.channels = wf.getnchannels()
    opts.rate = rate=wf.getframerate()
    audio = audio.AudioManager(opts)
    stream = p.open(format=opts.format,
                 channels=opts.channels,
                 rate=opts.rate,
                 output=True)
    print("____________Game mode____________")
    gamenum = 0
    correct = 0
    std = 0
    while gamenum < 10:
        distance = 1
        angle = random.randint(-90, 90)
        data = wf.readframes(opts.chunk)
        while data:
            data = audio.process(data,distance,angle)
            stream.write(data)
            data = wf.readframes(opts.chunk)
            if keyboard.is_pressed('q'):
                break
            
        wf.rewind()
        predict_angle = int(input("각도를 추측해보세요(-90 ~ 90): "))
        std = std + abs(predict_angle - angle)
        if abs(predict_angle - angle) < 10:
            print("정답입니다!")
            print("정답: ",angle)
            correct = correct + 1
        else:
            print("오답입니다!")
            print("정답: ",angle)       
        gamenum = gamenum + 1
        
    print("정답 횟수:",correct,"/10")
    print("평균 오차:",std/gamenum)
        
    
        
        
        
stream.stop_stream()
stream.close()
p.terminate()

