import argparse
import numpy as np
import pyaudio

class AudioOptions:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Audio options")
        
        self.parser.add_argument("--mode",
                                 type=str,
                                 help="player mode",
                                 default="realtime")
        self.parser.add_argument("--rate",
                                 type=int,
                                 help="sampling rate",
                                 default=16000)
        self.parser.add_argument("--format",
                                 type=int,
                                 help="formate",
                                 default=pyaudio.paInt16)   
        self.parser.add_argument("--channels",
                                 type=int,
                                 help="number of audio speaker",
                                 default=1)    
        self.parser.add_argument("--chunk",
                                 type=int,
                                 help="size of audio buffer",
                                 default=1600)  
        self.parser.add_argument("--device",
                                 type=int,
                                 help="input device index",
                                 default=0)
        self.parser.add_argument("--dtype",
                                 type=type,
                                 help="input device index",
                                 default=np.int16) 
        self.options = self.parser.parse_args()
        
    def parse(self):
        return self.options