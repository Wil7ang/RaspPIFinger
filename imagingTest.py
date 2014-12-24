import cv2
import numpy as np

import cv2
import numpy as np

camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

cv2.namedWindow('Frame')

while(True):
	ret,frame = camera.read()
	print frame[200][5]
	#for x in range(frame.shape[0],0,-1):
		#print frame[x]
	cv2.circle(frame,(200,5),2,(255,255,255,255),2)

	cv2.imshow('Frame',frame)

	if(cv2.waitKey(1) == ord('q')):
		break
camera.release()
cv2.destroyAllWindows()