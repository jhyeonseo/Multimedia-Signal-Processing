import cv2
import numpy as np
from matplotlib import pyplot as plt


def plot(img):
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])
    fig = plt.gcf()
    fig.canvas.draw()
    hist_image = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close()
    
    return hist_image


def equalize(img):
    ycrcb_image = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y_channel, cr_channel, cb_channel = cv2.split(ycrcb_image)
    equ_y_channel = cv2.equalizeHist(y_channel)
    equ_ycrcb_image = cv2.merge([equ_y_channel, cr_channel, cb_channel])
    output_image = cv2.cvtColor(equ_ycrcb_image, cv2.COLOR_YCrCb2BGR)
    
    return output_image
