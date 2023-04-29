import numpy as np
import random

def Uniform(img, gain):
    return np.clip(img + np.random.random((img.shape))*gain, 0, 255).astype(np.uint8)

def Salt(img, freq):
    output = np.copy(img)
    height, width = img.shape
    num_noise = int(width*height*freq)
    for i in range(num_noise):
        y=random.randint(0, height-1)
        x=random.randint(0, width-1)
        output[y][x] = 255
        
    return output

def Gaussian(img, mean, var):
    sigma = var ** 0.5
    gaussian = np.random.normal(mean, sigma, img.shape)
    return np.clip(img + gaussian, 0, 255).astype(np.uint8)
