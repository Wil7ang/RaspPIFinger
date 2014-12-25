import cv2
import numpy as np

import cv2
import numpy as np

def inRange(val,max,min):
    return val < max and val > min

camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

cv2.namedWindow('Frame')

columnNumberForPipe = 80

while(True):
    ret,frame = camera.read()
    # print frame[columnNumberForPipe][200]
    for x in range(220,0,-1):
        if(not inRange(frame[columnNumberForPipe][x][0], 80, 50) and \
           not inRange(frame[columnNumberForPipe][x][1],230,190) and \
           not inRange(frame[columnNumberForPipe][x][2],230,190)):
            cv2.circle(frame,(x,columnNumberForPipe),2,(0,0,255,255),2)
            break            

    cv2.imshow('Frame',frame)

    if(cv2.waitKey(1) == ord('q')):
        break
camera.release()
cv2.destroyAllWindows()