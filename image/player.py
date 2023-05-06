import cv2
import numpy as np
import filter
import noise
import fft_filter


FILTER = fft_filter.FFT_FILTER()
cap = cv2.VideoCapture("./data/people2.mp4")

while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)/255
        frame = cv2.resize(frame, (512, 512))
        

        i_gray, H = FILTER.filter_ft(frame, 0.25)
        cframe = np.hstack((frame, i_gray, H))
        cv2.imshow('2D-FFT', cframe)
        key = cv2.waitKey(33)
        if key == ord('q'):
            break
    
    
cap.release()
cv2.destroyAllWindows()