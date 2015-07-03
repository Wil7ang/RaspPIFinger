
################################################################################
# Goal of this is to get the program to find the bird and pipes
# on a screenshot of the flappy bird input from the video camera

# TODO:
# -get the image processor to know something about previous image
# need video for this to work
################################################################################

import cv2
import numpy as np
from matplotlib import pyplot as plt
from utils import apply_transform, find_object, crop, shift
import time

#some constants for cropping the img
BIRD_EDGE = 52
PIPE_SEPARATION_WIDTH = 103
PIPE_SEPARATION_HEIGHT = 135
PIPE_CEILING = 220  # to prevent accidentally finding the number as pipe
# error bound for detecting the second pipe, 
DELTA = 2

def run_tests():
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

    #gets the templates to do template matching with
    template = cv2.cvtColor(cv2.imread('template.jpg'), cv2.COLOR_BGR2GRAY)
    sample = screenshots[0]
    bird = apply_transform(template, sample, ((399, 350), (580, 500), (200, 55), (220, 85)))

    sample = screenshots[1]
    pipe = apply_transform(template, sample, ((564, 32), (837, 157), (229, 140), (250, 185)))

    # Does the processing, currently draws rectangles around where the program things the
    # object is. Takes ~4ms/image
    # Note can use for performance testing or sanity test.
    # for performance, comment out display stuff and increase num_trials
    # for sanity test, set num_trials=1 and uncomment display stuff
    total_times = [0] * len(screenshots)
    num_trials = 1
    for i in range(num_trials):
        for j in range(len(screenshots)):
            background = screenshots[j]
            t0 = time.time()

            background = cv2.warpAffine(background, affineM, (cols, rows))
            background_copy = background.copy()

            find_bird(bird, background_copy)
            find_pipes(pipe, background_copy)

            total_times[j] += time.time() - t0

            
            # display stuff. If you use this, please set num_trials to 1

            t0 = time.time()
            plt.subplot(111),plt.imshow(background_copy, cmap = 'gray')
            print 'display took: {}ms'.format((time.time() - t0) * 1000)
            plt.show()
            plt.close()
            

    for i in range(len(screenshots)):
        print 'running {} trials for image {} took {} seconds'\
            .format(num_trials, i, total_times[i])

# finds the bird
def find_bird(bird, background):
    # crop image
    bird_rows, bird_cols = bird.shape
    crop_bg = background[BIRD_EDGE:BIRD_EDGE + bird_rows + 10, :]

    res, min_val, max_val, top_left, bottom_right = find_object(bird, crop_bg)

    top_left = (top_left[0], top_left[1] + BIRD_EDGE)
    bottom_right = (bottom_right[0], bottom_right[1] + BIRD_EDGE)
    cv2.rectangle(background, top_left, bottom_right, (0,0,0), 2)

# finds the set of pipes. Note this algorithm only finds one set of pipes at a time.
# Not really a problem though because of where it looks ,there is always only 1 pipe set
def find_pipes(pipe, background):
    # first pipe, this takes ~2-2.5 ms to complete, so can do further cropping to reduce
    # time, see TODO
    t1 = time.time()
    crop_bg0 = background[BIRD_EDGE:, :PIPE_CEILING]

    res0, min_val0, max_val0, top_left0, bottom_right0 = find_object(pipe, crop_bg0)
    top_left0 = shift(top_left0, (0, BIRD_EDGE))
    bottom_right0 = shift(bottom_right0, (0, BIRD_EDGE))

    cv2.rectangle(background, top_left0, bottom_right0, (0,0,0), 2)

    # for finding the second pipe, looks up and down, then finds the closest match
    min_x = top_left0[0] - DELTA + PIPE_SEPARATION_WIDTH
    max_x = bottom_right0[0] + DELTA + PIPE_SEPARATION_WIDTH
    min_y = top_left0[1] - DELTA
    max_y = bottom_right0[1] + DELTA

    crop_bg1 = crop(background, min_x, max_x, min_y, max_y)

    if crop_bg1.shape[0] > pipe.shape[0] and crop_bg1.shape[1] > pipe.shape[1]:
        res1, min_val1, max_val1, top_left1, bottom_right1 = find_object(pipe, crop_bg1)
        corner = min_x, min_y
        top_left1 = shift(corner, top_left1)
        bottom_right1 = shift(corner, bottom_right1)
    else:
        max_val1 = 0

    min_x = top_left0[0] - DELTA - PIPE_SEPARATION_WIDTH
    max_x = bottom_right0[0] + DELTA - PIPE_SEPARATION_WIDTH
    min_y = top_left0[1] - DELTA
    max_y = bottom_right0[1] + DELTA

    crop_bg2 = crop(background, min_x, max_x, min_y, max_y)

    if crop_bg2.shape[0] > pipe.shape[0] and crop_bg2.shape[1] > pipe.shape[1]:
        res2, min_val2, max_val2, top_left2, bottom_right2 = find_object(pipe, crop_bg2)
        corner = min_x, min_y
        top_left2 = shift(corner, top_left2)
        bottom_right2 = shift(corner, bottom_right2)
    else:
        max_val2 = 0

    if max_val1 > max_val2:
        cv2.rectangle(background, top_left1, bottom_right1, (0,0,0), 2)
    else:
        cv2.rectangle(background, top_left2, bottom_right2, (0,0,0), 2)

#may swtich to main class later, but this is easy
run_tests()
