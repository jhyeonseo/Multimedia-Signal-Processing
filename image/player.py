import cv2
import numpy as np
import filter
import noise
import fft_filter
import histogram


FILTER = fft_filter.FFT_FILTER()
cap = cv2.VideoCapture("./data/people2.mp4")
cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)


while True:
    ret, frame = cap.read()
    if ret:
        cframe = histogram.plot(frame)
        cv2.imshow('Image', frame)
        cv2.imshow('Histogram', cframe)
        key = cv2.waitKey(33)
        if key == ord('q'):
            break
    
    
cap.release()
cv2.destroyAllWindows()