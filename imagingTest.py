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

    args = np.argsort(frame[columnNumberForPipe][90:230])

    blackLoc = 90 + args[3]#np.argmin(frame[columnNumberForPipe][90:220])
    cv2.circle(frame,(blackLoc,columnNumberForPipe),2,(0,0,255,255),2)

    cv2.imshow('Frame',frame)

    if(cv2.waitKey(1) == ord('q')):
        break

camera.release()
cv2.destroyAllWindows()
