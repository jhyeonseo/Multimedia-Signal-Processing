import numpy as np

def MovingAverage(kernel_size):
    return np.ones((kernel_size, kernel_size), np.float32)/(kernel_size*kernel_size)

def Laplacian(option='e'):
    if option == 'e':
        return np.array([[1,1,1],[1,-8,1],[1,1,1]])
    else:
        return np.array([[0,1,0],[1,-4,1],[0,1,0]])