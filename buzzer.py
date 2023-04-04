import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buzzer_pin = 12
GPIO.setup(buzzer_pin, GPIO.OUT)

pwm = GPIO.PWM(buzzer_pin, 1000)
pwm.start(50)

while True:
    try:
        pwm.ChangeFrequency(1000)
        print("aa")
        time.sleep(0.5)
        pwm.ChangeFrequency(500)
        time.sleep(0.5)
    except KeyboardInterrupt:
        break

pwm.stop()
GPIO.cleanup()
