import cv2
import numpy as np

def gammaCorrect1(im , gamma ):
    outImg = np.zeros(im.shape,im.dtype)
    rows,cols = im.shape
    for i in range(rows):
        for j in range(cols):
            outImg[i][j] = ( (im[i][j]/255.0) ** (1/gamma) )*255
    return outImg

def gammaCorrect2(im , gamma ):
    outImg = np.zeros(im.shape,im.dtype)
    rows,cols = im.shape
    for i in range(rows):
        for j in range(cols):
            gammaValue = ( (im.item(i,j)/255.0) ** (1/gamma) ) * 255
    outImg.itemset(i,j,gammaValue)
    return outImg

def gammaCorrect3(im , gamma ):
    outImg = np.zeros(im.shape,im.dtype)
    rows,cols = im.shape
    LUT = []
    for i in range(256):
        LUT.append( ( (i/255.0) ** (1/gamma) ) * 255 )

    for i in range(rows):
        for j in range(cols):
            gammaValue = LUT[im.item(i,j)]
            outImg.itemset(i,j,gammaValue)
    return outImg

def gammaCorrect4(im, gamma):
    outImg = np.zeros(im.shape, im.dtype)
    rows, cols = im.shape
    LUT = []
    for i in range(256):
        LUT.append(((i / 255.0) ** (1 / gamma)) * 255)
    LUT = np.array(LUT,dtype=np.uint8)
    outImg = LUT[im]
    return outImg
