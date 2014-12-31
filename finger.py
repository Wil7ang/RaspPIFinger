import cv2
import numpy as np
import datetime as dt
import time
import itertools

from RPIO import PWM


camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

cv2.namedWindow('Frame')

min_height = 20
max_height = 220
pipe_col = 86
bird_col = 195
pipes = []
frames_seen = 0
last_loc = 0
catch_time = dt.datetime.now()
start_time = dt.datetime.now()
target_height = 160
target_center = 30

def detect_bird(frame, local_min=min_height, local_max=max_height):
    return local_min + np.argmin(frame[bird_col][local_min:local_max])


def detect_pipe(frame):
    args = np.argsort(frame[pipe_col][90:220])[0:5]
    args = np.sort(args)[::-1]
    return 90 + args[0]


def set_target_range(frame, pipe_loc):
    global last_loc, target_height, start_time, catch_time, frames_seen, pipes
    if (dt.datetime.now() - start_time).total_seconds()*1000 > 150:
        if(frame[pipe_col][pipe_loc] < 100 and frames_seen == 0):
            last_loc = pipe_loc
            catch_time = dt.datetime.now()
            frames_seen += 1
        elif frames_seen > 0:
            if abs(pipe_loc - last_loc) < 7:
                frames_seen += 1
            else:
                frames_seen = 0

        if frames_seen >= 3:
            pipes.append([last_loc, pipe_col, catch_time, False])
            frames_seen = 0
            start_time = dt.datetime.now()

    # Remove offscreen pipes
    for index, pip in enumerate([pipe for pipe in pipes if
                                 (dt.datetime.now() - pipe[2]).total_seconds()*1000 > 800]):
        pipes.pop(index)

    # Check against pipes on screen.
    for pipe in pipes:
        if(not pipe[3] and (dt.datetime.now() - pipe[2]).total_seconds()*1000 > 400):
            pipe[3] = True
            target_height = pipe[0] - 15
            break


JUMP_HEIGHT = 30
clicks = 0
PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)
servo = PWM.Servo()
servo.set_servo(18, 1800) # Initialize starting position for the first click.
last_click = dt.datetime.now()
toggle_click = itertools.cycle(range(2)).next

def click(frame, direction, delay=300):
    # Range is from 500 to 2400
    # Swing for clicking is alternating from 1200 to 1800.
    global last_click
    if (dt.datetime.now() - last_click).total_seconds()*1000 < delay:
        return

    if direction:
        servo.set_servo(18, 1800)
    else:
        servo.set_servo(18, 1200)
    cv2.circle(frame, (160,120), 50, (0,255,0,255), 100)
    last_click = dt.datetime.now()


def main():
    last_click = dt.datetime.now()

    while(True):
        ret, frame = camera.read()
        grey = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)

        bird_loc = detect_bird(grey, local_min=target_height-75, local_max=target_height)

        cv2.circle(frame, (bird_loc, bird_col), 2, (0, 0, 255, 255), 2)

        pipe_loc = detect_pipe(grey)

        set_target_range(grey, pipe_loc)

        if bird_loc > target_height - target_center:
            click(frame, toggle_click(), 100 + 100 * (1 - (abs(bird_loc - target_height - target_center) /
                                                    float(abs(
                                                        max_height - target_height - target_center)))) ** 2)

        cv2.line(frame, (target_height - target_center, 0), (target_height - target_center, 240), (0, 255, 0, 0), 2)
        cv2.line(frame, (target_height, 0), (target_height, 240), (0, 0, 255, 255), 2)
        cv2.line(frame, (target_height-75, 0), (target_height-75, 240), (0, 0, 255, 255), 2)

        cv2.imshow('Frame', frame)

        if(cv2.waitKey(1) == ord('q')):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
