import time
import RPi.GPIO as GPIO

buzzer = 2
pinBtn = 18
led = 3

GPIO.setmode(GPIO.BCM)  # Configurer la numérotation des broches en BCM
GPIO.setwarnings(True)

GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(pinBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def sonner_buzzer():
    while True:
        GPIO.output(led, GPIO.HIGH)
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led, GPIO.LOW)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(1)


def buzzer_correct():
    for i in range(1, 4):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(0.08)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(0.09)


def buzzer_incorrect():
    GPIO.output(buzzer, GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(buzzer, GPIO.LOW)
    time.sleep(0.25)
    for i in range(0, 2):
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(0.12)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(0.12)


def led_on():
    GPIO.output(led, GPIO.HIGH)


def led_off():
    GPIO.output(led, GPIO.LOW)


def bouton_appuye(channel):
    serveur.est
