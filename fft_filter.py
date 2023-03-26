import numpy as np
from scipy import signal
from scipy.io import wavfile
import sys
WL = 256
WR = 128
def stft(x, w, step):
    wlen = len(w)
    nsampl = len(x)
    Xtf = np.array([np.fft.rfft(w*x[i:i+wlen])for i in range(0, nsampl - wlen + 1, step)]) + 1e-12*(1+1j)
    return Xtf

def istft(Xtf, w, step, nsampl):
    nframe = len(Xtf)
    wlen = len(w)
    y = np.zeros(nsampl)
    ws = np.zeros(nsampl)
    ind = 0
    for i in range(0, nsampl - wlen + 1, step):
        y[i:i + wlen] += w*np.fft.irfft(Xtf[ind])
        ws[i:i+wlen] += w*w
        ind += 1
        
    ws[ws==0] = 1
    y = y / ws
    return y
    
def filter_ft(mag, fcut, ftype):
    Nf, ft_bin = mag.shape
    fmag = np.zeros([Nf, ft_bin])
    if ftype=='lowpass':
        fcut_pos = int(ft_bin*fcut)
        fmag[:,0:fcut_pos]=mag[:,0:fcut_pos]
    elif ftype=='highpass':
        fcut_pos = int(ft_bin*fcut)
        fmag[:,fcut_pos:ft_bin]=mag[:,fcut_pos:ft_bin]  
    elif ftype=='bandpass':
        fcut_pos1 = int(ft_bin*fcut[0])
        fcut_pos2= int(ft_bin*fcut[1])
        fmag[:,fcut_pos1:fcut_pos2]=mag[:,fcut_pos1:fcut_pos2]
    elif ftype=='bandstop':
        fcut_pos1 = int(ft_bin*fcut[0])
        fcut_pos2= int(ft_bin*fcut[1])
        fmag[:,0:fcut_pos1]=mag[:,0:fcut_pos1]
        fmag[:,fcut_pos2:ft_bin]=mag[:,fcut_pos2:ft_bin]        
    return fmag
    
fs, data = wavfile.read(sys.argv[1])
ftype = sys.argv[-1]
if ftype=='bandpass' or ftype=='bandstop':
    fcut = [float(sys.argv[-3]), float(sys.argv[-2])]
else:
    fcut = float(sys.argv[3])
w = signal.hann(WL)
Xf = stft(data, w, WR)
Mag = np.abs(Xf)
Phs = np.angle(Xf)
fMag = filter_ft(Mag, fcut, ftype)
Xfr = fMag*np.exp(1j * Phs)
y = istft(Xfr, w, WR, len(data))
wavfile.write(sys.argv[2], fs, y.astype(np.int16))
