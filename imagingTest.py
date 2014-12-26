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
    frame = cv2.cvtColor(frame,cv2.cv.CV_BGR2GRAY)
    #print frame[columnNumberForPipe][np.argmin(frame[columnNumberForPipe])]
    blackLoc = 60 + np.argmin(frame[columnNumberForPipe][60:220])
    cv2.circle(frame,(blackLoc,columnNumberForPipe),2,(0,0,255,255),2)
    # print frame[columnNumberForPipe][220]
    # for x in range(220,60,-1):
    #     if(inRange(frame[columnNumberForPipe][x][0],140, 0) and \
    #        inRange(frame[columnNumberForPipe][x][1],140, 0) and \
    #        inRange(frame[columnNumberForPipe][x][2],140, 0)):
    #         cv2.circle(frame,(x,columnNumberForPipe),2,(0,0,255,255),2)
    #         break


    cv2.imshow('Frame',frame)

    if(cv2.waitKey(1) == ord('q')):
        break
camera.release()
cv2.destroyAllWindows()