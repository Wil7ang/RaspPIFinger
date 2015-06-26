#goal is to get the whole enchilada working (on a template at least)

import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils import apply_transform
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

sample = screenshots[1]
up_pipe = apply_transform(template, sample, ((564, 32), (837, 157), (229, 140), (250, 185)))

down_pipe = apply_transform(template, sample, ((562, 667), (834, 792), (128, 140), (147, 184)))

method = cv2.TM_CCOEFF



for img in [bird, up_pipe, down_pipe]:
    for background in screenshots:
        t0 = time.time()

        background_copy = background.copy()

        res = cv2.matchTemplate(img, background, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        h, w = img.shape
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(background_copy, top_left, bottom_right, (0,0,0), 2)

        plt.subplot(121),plt.imshow(res, cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(background_copy, cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(method)

        background = background_copy.copy()

        plt.show()

        plt.close()

        print 'this took: {} seconds'.format(time.time() - t0)

