import cv2
import numpy as np

from RPIO import PWM


camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

cv2.namedWindow('Frame')

min_height = 20
max_height = 220
columnNumberForPipe = 80
bird_col = 195

def detect_bird(frame):
    return min_height + np.argmin(frame[bird_col][min_height:max_height])


JUMP_HEIGHT = 30
clicks = 0
servo = PWM.Servo()
servo.set_servo(18, 1800) # Initialize starting position for the first click.

def click():
    # Range is from 500 to 2400
    # Swing for clicking is alternating from 1200 to 1800.
    global clicks
    clicks += 1
    if clicks%2 == 0:
        servo.set_servo(18, 1200)
    else:
        servo.set_servo(18, 1800)


def main():
    while(True):
        ret,frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY)

        detect_bird(frame)

        cv2.imshow('Frame', frame)

        if(cv2.waitKey(1) == ord('q')):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
