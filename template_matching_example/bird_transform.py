#uses an affine transform to transform the screenshot images to a rectange.
#points were determined by hand. Too lazy to write algorithm as the
#camera doesn't move that much...
import cv2
import numpy as np
from matplotlib import pyplot as plt

#get images
images = []
for i in range(4):
	img = cv2.imread('screenshot{}.png'.format(i))
	images.append(img)

pointSet1 = np.float32([[0,0],[320,0],[0, 240]])
pointSet2 = np.float32([[29,25],[289,27],[26,220]])
M = cv2.getAffineTransform(pointSet2, pointSet1)
rows,cols,ch = images[0].shapesw

for image in images:
	dst = cv2.warpAffine(image,M,(cols, rows))

	plt.subplot(121)
	plt.imshow(image, cmap='gray')
	plt.title('Input')
	plt.subplot(122)
	plt.imshow(dst, cmap='gray')
	plt.title('Output')
	plt.show()