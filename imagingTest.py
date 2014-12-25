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

rowForPipe = 120

while(True):
    ret,frame = camera.read()
    # print frame[15][150]
    # for y in range(20,):
    #     if(not inRange(frame[y][rowForPipe][0], 80, 60) and \
    #        not inRange(frame[y][rowForPipe][1],170,150) and \
    #        not inRange(frame[y][rowForPipe][2],170,150)):
    #         cv2.circle(frame,(x,15),2,(0,0,255,255),2)
    #         break    
    cv2.circle(frame,(rowForPipe,20),2,(0,0,255,255),2)        

    cv2.imshow('Frame',frame)

    if(cv2.waitKey(1) == ord('q')):
        break
camera.release()
cv2.destroyAllWindows()