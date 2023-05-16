import RPi.GPIO as GPIO
import random

pinBtn = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinBtn, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
    GPIO.wait_for_edge(18, GPIO.FALLING)

    print("AAAAAAAAAAAAAAAAA")
