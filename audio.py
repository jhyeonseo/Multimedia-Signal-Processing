import numpy as np
import scipy.signal as signal
import fplot

class AudioManager:
    def __init__(self,options):
        self.opt=options
        self.filter=Filter()
        self.past_data=np.zeros(self.filter.tap-1,dtype=self.opt.dtype)
        
    def process(self,input):
        # 과거 input의 마지막 data를 처음 부분에 연결
        in_data = np.concatenate((self.past_data,np.fromstring(input,dtype=self.opt.dtype)))
        # 현재 input의 마지막 data를 저장
        self.past_data = in_data[in_data.size-(self.filter.tap-1):]
        # 필터링 수행
        if self.filter.type != None:
            out_data = np.convolve(in_data,self.filter.kernel,mode='valid').astype(self.opt.dtype)
        else:
            out_data = in_data
        return out_data.tostring()

    
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
            
            
        
        
