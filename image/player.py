import cv2
import numpy as np
import filter
import noise

kernel = filter.MovingAverage(11)
cap = cv2.VideoCapture("./data/people2.mp4")

# 창 이름 지정
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
# 창 크기 조절
cv2.resizeWindow('Image', 1200, 1200)

while True:
    ret, frame = cap.read()
    if ret:
        t_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        Y, Cr, Cb = cv2.split(t_frame)
        noisy = noise.Gaussian(Y, 0,100)
        filtered = cv2.filter2D(noisy, -1, kernel)
        cnoisy = cv2.cvtColor(cv2.merge((noisy, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
        cfiltered = cv2.cvtColor(cv2.merge((filtered, Cr, Cb)), cv2.COLOR_YCrCb2BGR)
        cframe = np.hstack((frame, cnoisy, cfiltered))
        cv2.imshow('Image', cframe)




        key = cv2.waitKey(0)
        if key == ord('q'):
            break
    
    
cap.release()
cv2.destroyAllWindows()