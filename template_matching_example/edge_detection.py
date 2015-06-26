#run the edge detection

import cv2
import numpy as np
from matplotlib import pyplot as plt

images = []
for i in range(4):
	img = cv2.imread('screenshot{}.png'.format(i))
	images.append(img)

for image in images:
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 100, 200, apertureSize=3)

	plt.subplot(121)
	plt.imshow(gray, cmap='gray')
	plt.subplot(122)
	plt.imshow(edges, cmap='gray')
	plt.show()

#corner detection. Doesn't really work...
#designed for different sorts of corners. Read wiki
#for details
for image in images:
	break
	plt.subplot(121)

	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gray = np.float32(gray)

	plt.imshow(gray, cmap='gray')

	dst = cv2.cornerHarris(gray,2,3,0.01)

	dst = cv2.dilate(dst,None)

	img[dst>0.001*dst.max()]=[0,0,255]


	plt.subplot(122)
	plt.imshow(dst, cmap = 'gray')
	plt.title('Result')
	plt.xticks([])
	plt.yticks([])

	plt.show()