# tests/test_motors.py
# !! Keep wheels OFF the ground before running this !!

import RPi.GPIO as GPIO
import time

ENA, IN1, IN2 = 18, 23, 24
ENB, IN3, IN4 = 13, 25, 8

GPIO.setmode(GPIO.BCM)
for p in (ENA, IN1, IN2, ENB, IN3, IN4):
    GPIO.setup(p, GPIO.OUT)

pwm_a = GPIO.PWM(ENA, 1000)
pwm_b = GPIO.PWM(ENB, 1000)
pwm_a.start(0)
pwm_b.start(0)

def left(direction, speed):
    GPIO.output(IN1, direction > 0)
    GPIO.output(IN2, direction < 0)
    pwm_a.ChangeDutyCycle(abs(speed))

def right(direction, speed):
    GPIO.output(IN3, direction > 0)
    GPIO.output(IN4, direction < 0)
    pwm_b.ChangeDutyCycle(abs(speed))

try:
    print('Forward 50%...')
    left(+1, 50); right(+1, 50); time.sleep(2)

    print('Stop...')
    left(0, 0); right(0, 0); time.sleep(1)

    print('Reverse 50%...')
    left(-1, 50); right(-1, 50); time.sleep(2)

    print('Spin in place...')
    left(+1, 50); right(-1, 50); time.sleep(2)

    print('Done.')

finally:
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
