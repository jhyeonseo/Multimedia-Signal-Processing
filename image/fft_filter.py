import cv2
import numpy as np

class FFT_FILTER:      
    def __init__(self):
        self.kernel= {}
        self.kernel['type'] = None
        
        
    def fft(self, img, type=None):
        F = np.fft.fft2(img)
        Fshift = np.fft.fftshift(F)
    
        if type == 'visualize':
            return np.clip((20*np.log(np.abs(Fshift))),0,255).astype(np.uint8)
        else:
            return Fshift


    def ifft(self, img):
        iF_sh = np.fft.ifftshift(img)
        i_gray= np.clip(np.abs(np.fft.ifft2(iF_sh)),0,255)
        return i_gray
    
    
    def Build_H(self, N, f_radius):
        HN=N/2
        H = np.zeros((N, N), dtype=np.float32)
        for y in range(N):
            for x in range(N):
                fy=(y-HN)/HN
                fx=(x-HN)/HN
                radius = np.sqrt(fy*fy+fx*fx)
                if radius <= f_radius:
                    H[y][x] = 1
        return H


    def Filter2D_FT(self, Fin, H):
        mag = np.abs(Fin)
        phs = np.angle(Fin)
        fmag = H*mag
        return fmag*np.exp(1j * phs)

    
    def filter_ft(self, img, fcut, ftype='ideal'):
        if ftype=='ideal':
            if self.kernel['type'] == None:
                self.kernel['type'] = 'ideal'
                self.kernel['kernel'] = self.Build_H(img.shape[0], fcut)
                self.kernel['visualize'] = (self.kernel['kernel']*255).astype(np.uint8)
                
            FF = self.Filter2D_FT(self.fft(img), self.kernel['kernel'])
            output = self.ifft(FF)

  
        return output, self.kernel['visualize']


