#finds the flappy bird image in the background

import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

background = cv2.imread('background.jpg', 0)
background_copy = background.copy()

#Only really works if the match the object in the background is about the
#same size as the bird in the image
#bird = cv2.imread('bird.jpg', 0)
bird = cv2.imread('smaller_bird.jpg', 0)
h, w = bird.shape

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

plt.subplot(121), plt.imshow(bird, cmap='gray')
plt.subplot(122), plt.imshow(background, cmap='gray')
plt.suptitle('images used')
plt.show()

for m in methods:
    t0 = time.time()

    background = background_copy.copy()
    method = eval(m)

    res = cv2.matchTemplate(bird, background, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(background, top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(res, cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(background, cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(m)

    print 'this took: {} seconds'.format(time.time() - t0)

    plt.show()

    plt.close()