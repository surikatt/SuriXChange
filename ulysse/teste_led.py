import RPi.GPIO as GPIO
import time

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
GPIO.setup(26, GPIO.OUT)

while True:
    GPIO.output(26, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(26, GPIO.LOW)
    time.sleep(0.5)
