from RPIO import PWM

servo = PWM.Servo()

clicks = 0

def click():
    # Range is from 500 to 2400
    # Swing for clicking is alternating from 1200 to 1800.
    global clicks
    clicks++
    if clicks%2 == 0:
        servo.set_servo(18, 1200)
    else:
        servo.set_servo(18, 1800)
