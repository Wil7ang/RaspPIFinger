#goal is to get the whole enchilada working (on a template at least)

import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

#commented stuff is for displaying data
def apply_transform(template, sample, (pt1,pt2,pt3,pt4)):
    x1, y1 = pt1
    x2, y2 = pt2
    x3, y3 = pt3
    x4, y4 = pt4    
    
    '''
    template_copy = template.copy()
    sample_copy = sample.copy()
    
    cv2.rectangle(template, (x1, y1), (x2, y2), (0,0,0), 5)
    plt.subplot(121)
    plt.imshow(template, cmap='gray')

    print x3,y3,x4,y4
    cv2.rectangle(sample, (x3, y3), (x4, y4), (0,0,0), 1)
    plt.subplot(122)
    plt.imshow(sample, cmap='gray')
    plt.suptitle('boxes I used for the template matching')
    plt.show()

    template = template_copy.copy()
    sample = sample_copy.copy()
    '''
    ps1 = np.float32([[x1,y1],[x2,y2],[x1,y2]])
    rows = abs(y4-y3)
    cols = abs(x4-x3)
    ps2 = np.float32([[cols,0],[0,rows],[0,0]])
    img_affine = cv2.getAffineTransform(ps1, ps2)
    img = cv2.warpAffine(template, img_affine, (cols, rows))
    '''
    plt.subplot(121)
    plt.imshow(img, cmap='gray')
    plt.suptitle('result')
    plt.show()
    
    template = template_copy.copy()
    '''
    return img


def find_object(img, background):
    method = cv2.TM_CCOEFF_NORMED

    res = cv2.matchTemplate(img, background, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    h, w = img.shape

    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    return res, min_val, max_val, top_left, bottom_right

# handles invalid indices
def crop(img, x_min, x_max, y_min, y_max):
    img_rows, img_cols = img.shape

    y_min = max(0, y_min)
    y_max = min(img_rows - 1, y_max)
    x_min = max(0, x_min)
    x_max = min(img_cols - 1, x_max)

    return img[y_min: y_max, x_min: x_max]

def shift(point, shift):
    return point[0] + shift[0], point[1] + shift[1]

def scale(point, factor):
    return int(1.0 * point[0] * factor), int(1.0 * point[1] * factor)

# does all of the matlibplt stuff
def show(img):
    t0 = time.time()
    plt.subplot(111)
    plt.imshow(img, cmap = 'gray')
    print 'display took: {}ms'.format((time.time() - t0) * 1000)
    plt.show()
    plt.close()

def show2(img1, img2):
    plt.subplot(121)
    plt.imshow(img1, cmap='gray')
    plt.subplot(122)
    plt.imshow(img2, cmap='gray')
    plt.show()
    plt.close()








