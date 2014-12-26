import cv2
import numpy as np

def inRange(val,max,min):
    return val < max and val > min

camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

cv2.namedWindow('Frame')

columnNumberForPipe = 80

pipeArray = []

while(True):
    ret,frame = camera.read()
    frame = cv2.cvtColor(frame,cv2.cv.CV_BGR2GRAY)

    args = np.argsort(frame[columnNumberForPipe][90:220])[0:5]
    args = np.sort(args)
    args = args[::-1]

    blackLoc = 90 + args[0]#np.argmin(frame[columnNumberForPipe][90:220])
    if(frame[columnNumberForPipe][blackLoc] < 100):
        #cv2.circle(frame,(blackLoc,columnNumberForPipe),2,(0,0,255,255),2)
        pipeArray.append([blackLoc,columnNumberForPipe])

    for pipe in pipeArray:
        cv2.circle(frame,(pipe[0],pipe[1]),2,(0,0,255,255),2)
        pipe[1] = pipe[1] + 2



    cv2.imshow('Frame',frame)

    if(cv2.waitKey(1) == ord('q')):
        break

camera.release()
cv2.destroyAllWindows()
