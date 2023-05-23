import RPi.GPIO as GPIO
import time
from random import randint
 
SENSOR_PIN = 23

print("initialisation")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SENSOR_PIN, GPIO.IN)
 
def my_callback(channel):
    # Here, alternatively, an application / command etc. can be started.
    print(f'There was a movement! {randint(0, 100)}')
 
"""while True:
    a = GPIO.input(SENSOR_PIN)
    print(f'{a} {randint(0, 100)}')"""

try:
    GPIO.add_event_detect(SENSOR_PIN , GPIO.FALLING, callback=my_callback)
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    print ("Finish...")
GPIO.cleanup()
