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

catchTime = dt.datetime.now()

start = dt.datetime.now()
expectedBirdHeight = 160

def ProcessPipes(frame):
    global pipeArray, seenForFrames, lastLocation, catchTime, start, expectedBirdHeight
    
    grey = cv2.cvtColor(frame,cv2.cv.CV_BGR2GRAY)
    result = frame

    args = np.argsort(grey[columnNumberForPipe][90:220])[0:5]
    args = np.sort(args)
    args = args[::-1]

    blackLoc = 90 + args[0]

    if (dt.datetime.now() - start).microseconds/1000 > 150:
        if(grey[columnNumberForPipe][blackLoc] < 100 and seenForFrames == 0):
            lastLocation = blackLoc
            catchTime = dt.datetime.now()
            seenForFrames += 1
        elif seenForFrames > 0:
            if abs(blackLoc - lastLocation) < 7:
                seenForFrames += 1
            else:
                seenForFrames = 0

        if seenForFrames >= 3:
            pipeArray.append([lastLocation,columnNumberForPipe,catchTime,False])
            seenForFrames = 0
            start = dt.datetime.now()

    for index, pip in enumerate([pipe for pipe in pipeArray if (dt.datetime.now() - pipe[2]).microseconds/1000 > 800]):
        pipeArray.pop(index)

    for pipe in pipeArray:
        if(not pipe[3] and (dt.datetime.now() - pipe[2]).microseconds/1000 > 400):
            pipe[3] = True
            expectedBirdHeight = pipe[0] - 15
            break

    cv2.circle(result,(expectedBirdHeight,195),2,(0,0,255,255),2)
    cv2.line(result,(expectedBirdHeight,0),(expectedBirdHeight,240),(0,0,255,255),2)
    cv2.line(result,(expectedBirdHeight-75,0),(expectedBirdHeight-75,240),(0,0,255,255),2)


#     cv2.imshow('Frame',result)

#     if(cv2.waitKey(1) == ord('q')):
#         break

# camera.release()
# cv2.destroyAllWindows()
