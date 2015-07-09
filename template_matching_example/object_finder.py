
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
from utils import apply_transform, find_object, crop, shift, show, show2, scale
import time

#some constants for cropping the img
BIRD_EDGE = 0
PIPE_SEPARATION_WIDTH = 84
PIPE_SEPARATION_HEIGHT = 140
PIPE_CEILING = 220  # to prevent accidentally finding the number as pipe
# error bound for detecting the second pipe, 
DELTA = 2
RESIZE = .5

def run_tests():
    #get the screenshots
    screenshots = []
    for i in range(4):
        img = cv2.imread('screenshot{}.png'.format(i))
        #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        screenshots.append(img)

    #gets the templates to do template matching with
    template = cv2.cvtColor(cv2.imread('template.jpg'), cv2.COLOR_BGR2GRAY)
    sample = screenshots[0]
    bird = apply_transform(template, sample, ((399, 350), (580, 500), (189,73), (206, 96)))
    bird = cv2.resize(bird, (0,0), fx=RESIZE, fy=RESIZE)

    sample = screenshots[1]
    pipe = apply_transform(template, sample, ((564, 32), (837, 157), (214,139), (230, 176)))
    pipe = cv2.resize(pipe, (0,0), fx=RESIZE, fy=RESIZE)

    # Does the processing, currently draws rectangles around where the program things the
    # object is. Takes ~.6ms/image -> 24ms/image on the PI
    # Note can use for performance testing or sanity test.
    # for performance, comment out display stuff and increase num_trials
    # for sanity test, set num_trials=1 and uncomment display stuff
    total_times = [0] * len(screenshots)
    num_trials = 1000
    for i in range(num_trials):
        for j in range(len(screenshots)):
            background = screenshots[j]
            t0 = time.time()

            #hardcoded these values to make the program only focus on what I think is important
            img = background[70:200, 60:285]
            img = cv2.resize(img, (0,0), fx=RESIZE, fy=RESIZE)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            #background_copy = background.copy()

            bird_corners = find_bird(bird, img)
            top_left_bird, bottom_right_bird = scale_corners(bird_corners)

            pipe_corners = find_pipes(pipe, img)
            p0, p1, p2, p3 = scale_corners(pipe_corners)

            total_times[j] += time.time() - t0

            '''
            # display stuff. If you use this, please set num_trials to 1
            cv2.rectangle(background, top_left_bird, bottom_right_bird, (0,0,0), 1)
            cv2.rectangle(background, p0, p1, (0,0,0), 1)
            cv2.rectangle(background, p2, p3, (0,0,0), 1)
            show(background)
            '''

    for i in range(len(screenshots)):
        print 'running {} trials for image {} took {} seconds'\
            .format(num_trials, i, total_times[i])

def scale_corners(corners):
    result = []
    for point in corners:
        point = scale(point, 1/RESIZE)
        result.append(shift(point, (60,70)))
    return result


# finds the bird
def find_bird(bird, background):
    # crop image
    bird_rows, bird_cols = bird.shape
    crop_bg = background[BIRD_EDGE:BIRD_EDGE + bird_rows + 10 * RESIZE, :]

    res, min_val, max_val, top_left, bottom_right = find_object(bird, crop_bg)

    top_left = shift(top_left, (0,BIRD_EDGE))
    bottom_right = shift(bottom_right, (0,BIRD_EDGE))

    return top_left, bottom_right



# finds the set of pipes. Note this algorithm only finds one set of pipes at a time.
# Not really a problem though because of where it looks ,there is always only 1 pipe set
def find_pipes(pipe, background):
    # first pipe, this takes ~2-2.5 ms to complete, so can do further cropping to reduce
    # time, see TODO

    res0, min_val0, max_val0, top_left0, bottom_right0 = find_object(pipe, background)
    top_left0 = shift(top_left0, (0, BIRD_EDGE))
    bottom_right0 = shift(bottom_right0, (0, BIRD_EDGE))
    
    width = int(PIPE_SEPARATION_WIDTH * RESIZE)
    # for finding the second pipe, looks up and down, then finds the closest match
    min_x = top_left0[0] - DELTA + width
    max_x = bottom_right0[0] + DELTA + width
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
    
    min_x = top_left0[0] - DELTA - width
    max_x = bottom_right0[0] + DELTA - width
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
        return top_left0, bottom_right0, top_left1, bottom_right1
    else:
        return top_left0, bottom_right0, top_left2, bottom_right2
    

    

#may swtich to main class later, but this is easy
run_tests()
