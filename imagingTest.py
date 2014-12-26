import cv2
import numpy as np

def inRange(val,max,min):
    return val < max and val > min

camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

cv2.namedWindow('Frame')

min_height = 20
max_height = 220
columnNumberForPipe = 80
bird_col = 195

while(True):
    ret,frame = camera.read()
    frame = cv2.cvtColor(frame,cv2.cv.CV_BGR2GRAY)

    blackLoc = 80 + np.argmin(frame[columnNumberForPipe][80:max_height])
    cv2.circle(frame,(blackLoc,columnNumberForPipe),2,(0,0,255,255),2)

    bird_loc = min_height + np.argmin(frame[bird_col][min_height:max_height])
    cv2.circle(frame,(bird_loc, bird_col), 2, (0,255,255,255), 2)

    cv2.imshow('Frame',frame)

    if(cv2.waitKey(1) == ord('q')):
        break

camera.release()
cv2.destroyAllWindows()
