import cv2
import numpy as np

import cv2
import numpy as np

def inRange(val,max,min):
    return val < max and val < min

camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

cv2.namedWindow('Frame')

columnNumberForPipe = 15

while(True):
    ret,frame = camera.read()
    #print frame[150][15]
    for x in range(frame.shape[0],0,-1):
        if(not inRange(frame[x][columnNumberForPipe][0],107,95) and \
           not inRange(frame[x][columnNumberForPipe][1], 83,67) and \
           not inRange(frame[x][columnNumberForPipe][2], 74,60))):
            cv2.circle(frame,(x,15),(0,0,255,255),2,2)
            break            

    cv2.imshow('Frame',frame)

    if(cv2.waitKey(1) == ord('q')):
        break
camera.release()
cv2.destroyAllWindows()