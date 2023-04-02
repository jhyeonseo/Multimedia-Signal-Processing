import numpy as np
import scipy.signal as signal
import fplot

class AudioManager:
    def __init__(self,options):
        self.opt=options
        self.filter=Filter()
        #self.past_data=np.zeros(self.filter.tap-1,dtype=self.opt.dtype)
        self.aheadL = np.zeros(self.opt.chunk, dtype=np.int16)
        self.aheadR = np.zeros(self.opt.chunk, dtype=np.int16)       
        
    def process(self, input, distance=1, angle=0):
        '''
        # 과거 input의 마지막 data를 처음 부분에 연결
        in_data = np.concatenate((self.past_data,np.fromstring(input,dtype=self.opt.dtype)))
        # 현재 input의 마지막 data를 저장
        self.past_data = in_data[in_data.size-(self.filter.tap-1):]
        # 필터링 수행
        if self.filter.type != None:
            out_data = np.convolve(in_data,self.filter.kernel,mode='valid').astype(self.opt.dtype)
        else:
            out_data = in_data
        '''
        in_data = np.fromstring(input, dtype=self.opt.dtype)
        out_data = self.sound_rendering(in_data, distance=distance, angle=np.pi*float(angle)/180)
            
        return out_data.tostring()
    
    def sound_rendering(self, signal, distance, angle, head=10):
        eardistance = 2 * head * 0.01 * np.abs(np.sin(angle))
        delay = int(eardistance * self.opt.rate/339)
        max_delay = int(self.opt.rate*2*head*.01/339)
        if max_delay > self.opt.chunk:
            max_delay = self.opt.chunk
        out = np.zeros(len(signal), dtype=np.int16)

        if angle >= 0:
            for i in range(int(len(signal)/2)):
                if i < delay:
                    out[i*2] = self.aheadL[max_delay - delay + i]
                else:
                    out[i*2] = signal[(i-delay)*2]
                    
                out[i*2] = int(out[i*2]*(distance/(distance+eardistance)))
                out[i*2+1] = signal[i*2]
        else:
            for i in range(int(len(signal)/2)):
                if i < delay:
                    out[i*2+1] = self.aheadR[max_delay - delay + i]
                else:
                    out[i*2+1] = signal[(i-delay)*2]
                out[i*2+1] = int(out[i*2+1]*(distance/(distance+eardistance)))
                out[i*2] = signal[i*2]
                
        for i in range(max_delay):
            self.aheadL[i] = signal[(int(len(signal)/2) - max_delay + i)*2]
            self.aheadR[i] = signal[(int(len(signal)/2) - max_delay + i)*2]
        
        return out
    
    def select_channel(self, signal, ch='right'):
        out = np.zeros(int(len(signal)/2), dtype=np.int16)
        for i in range(self.opt.chunk):
            if ch=='left':
                out[i*2]=signal[i*2]
                out[i*2+1]=0
            else:
                out[i*2]=0
                out[i*2+1]=signal[i*2]
                
        return out

    
    def change(self):
        self.filter.change()
        self.show()
        
        
    def show(self):
        print("Current filter options")
        if self.filter.type == None:
            print("No filter")
        else:
            print("*************************")
            print("Type: ", self.filter.type)
            print("Taps: ", self.filter.tap)
            if self.filter.pass_zero == 'bandpass' or self.filter.pass_zero == 'bandstop':  
                print("Cutoff: ", self.filter.cutoff, "(", self.filter.cutoff[0]*self.opt.rate/2,"Hz,", self.filter.cutoff[1]*self.opt.rate/2, "Hz )")
            else:
                print("Cutoff: ", self.filter.cutoff, "(", self.filter.cutoff*self.opt.rate/2, "Hz)")
            print("Window: ", self.filter.window)
            print("Pass zero: ", self.filter.pass_zero)
            print("*************************")
            fplot.mfreqz(self.filter.kernel)
            fplot.show()
        

class Filter:
    def __init__(self,type=None,tap=1,cutoff=None,window=None,pass_zero=None):
        self.type = type
        self.tap = tap
        self.cutoff = cutoff
        self.window = window
        self.pass_zero = pass_zero
            
    def change(self):
        print("Change Filter Option")
        
        # Filter type
        key = int(input("1: None  2: FIR  3: IIR  4: Moving average\n"))
        if key == 1:
            self.type = None
            return
        elif key == 2:
            self.type = 'FIR'
        elif key == 3:
            self.type = 'IIR'
        elif key == 4:
            self.type = 'Moving average'
            self.tap = int(input("Tap: "))
            self.kernel = np.full(self.tap,1/self.tap)
            self.pass_zero = 'losspass'
            self.cutoff = 1/self.tap
            self.window = None
            return
        else:
            print("ERROR: wrong type")
            return
        
        # Filter taps
        self.tap = int(input("Tap: "))
        
        # Pass zero
        key = int(input("1: lowpass  2: highpass  3: bandpass  4: bandstop\n"))
        if key == 1:
            self.pass_zero = 'lowpass'
        elif key == 2:
            self.pass_zero = 'highpass'
        elif key == 3:
            self.pass_zero = 'bandpass'
        elif key == 4:
            self.pass_zero = 'bandstop'
        else:
            print("ERROR: wrong pass zero")
            return   
        
        # Cutoff   0 ~ 1(Nyquist frequency)
        if self.pass_zero == 'bandpass' or self.pass_zero == 'bandstop':
            cutoff1 = float(input("cutoff1: "))
            cutoff2 = float(input("cutoff2: "))
            self.cutoff=[cutoff1,cutoff2]
        else:
            self.cutoff = float(input("cutoff: "))
        
        # Window
        key = int(input("1: Rectangular  2: Hamming  3: Triangular  4: Blackman\n"))
        if key == 1:
            self.window = 'boxcar'
        elif key == 2:
            self.window = 'hamming'
        elif key == 3:
            self.window  = 'triang'
        elif key == 4:
            self.window = 'blackman'
        else:
            print("ERROR: wrong window")
            return  
        
        print(self.cutoff)
        self.kernel = signal.firwin(self.tap,cutoff=self.cutoff,window=self.window,pass_zero=self.pass_zero)
            
            
        
        
