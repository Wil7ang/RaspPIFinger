import cv2
import numpy as np
import datetime as dt

def inRange(val,max,min):
    return val < max and val > min

camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

cv2.namedWindow('Frame')

columnNumberForPipe = 80

pipeArray = []

seenForFrames = 0
lastLocation = 0

start = dt.datetime.now()
end = dt.datetime.now()

while(True):
    ret,frame = camera.read()
    frame = cv2.cvtColor(frame,cv2.cv.CV_BGR2GRAY)

    args = np.argsort(frame[columnNumberForPipe][90:220])[0:5]
    args = np.sort(args)
    args = args[::-1]

    blackLoc = 90 + args[0]#np.argmin(frame[columnNumberForPipe][90:220])

    if (dt.datetime.now() - start).microseconds/1000 > 150:
        if(frame[columnNumberForPipe][blackLoc] < 100 and seenForFrames == 0):
            lastLocation = blackLoc
            seenForFrames += 1
        elif seenForFrames > 0:
            if abs(blackLoc - lastLocation) < 5:
                seenForFrames += 1
            else:
                seenForFrames = 0

        if seenForFrames >= 3:
            pipeArray.append([lastLocation,columnNumberForPipe])
            seenForFrames = 0
            start = dt.datetime.now()

        #cv2.circle(frame,(blackLoc,columnNumberForPipe),2,(0,0,255,255),2)
        # pipeArray.append([blackLoc,columnNumberForPipe])

    for index, pip in enumerate([for pipe in pipeArray if pipe[1] > 240]):
        pipeArray.pop(index)

    for pipe in pipeArray:
        cv2.circle(frame,(pipe[0],pipe[1]),2,(0,0,255,255),2)
        pipe[1] = pipe[1] + 4


    cv2.imshow('Frame',frame)

    if(cv2.waitKey(1) == ord('q')):
        break

camera.release()
cv2.destroyAllWindows()
