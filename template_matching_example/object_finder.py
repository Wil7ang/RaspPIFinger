#goal is to get the whole enchilada working (on a template at least)

import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils import apply_transform, find_object
import time

#get the screenshots
screenshots = []
for i in range(4):
	img = cv2.imread('screenshot{}.png'.format(i))
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	screenshots.append(img)

#affine trans to get screenshots onto rectangle
pointSet1 = np.float32([[0,0],[320,0],[0, 240]])
pointSet2 = np.float32([[29,25],[289,27],[26,220]])

affineM = cv2.getAffineTransform(pointSet2, pointSet1)
rows,cols= screenshots[0].shape

screenshots = map(lambda img: cv2.warpAffine(img, affineM, (cols, rows)), screenshots)

#gets the templates to do template matching with
template = cv2.cvtColor(cv2.imread('template.jpg'), cv2.COLOR_BGR2GRAY)
sample = screenshots[0]
bird = apply_transform(template, sample, ((399, 350), (580, 500), (200, 55), (220, 85)))
bird_rows, bird_cols = bird.shape

sample = screenshots[1]
pipe = apply_transform(template, sample, ((564, 32), (837, 157), (229, 140), (250, 185)))
pipe_rows, pipe_cols = pipe.shape

bird_edge = 52  # the estimated start of the bird for template finding, am generous
pipe_separation = 85  # about how many pixels the pipes are apart

method = cv2.TM_CCOEFF

for img in [bird, pipe]:
    for background in screenshots:
        t0 = time.time()

        background_copy = background.copy()
        res, min_val, max_val, top_left, bottom_right = find_object(img, background)
        
        cv2.rectangle(background_copy, top_left, bottom_right, (0,0,0), 2)

        print 'math took: {} seconds'.format(time.time() - t0)
        t0 = time.time()

        plt.subplot(121),plt.imshow(res, cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(background_copy, cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(method)

        background = background_copy.copy()

        print 'display took: {} seconds'.format(time.time() - t0)

        plt.show()

        plt.close()

