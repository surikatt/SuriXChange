import RPi.GPIO as GPIO
import time
from multiprocessing import Process

led = 3  # Broche GPIO à laquelle la LED est connectée =>5
buzzer = 2 # => 13

GPIO.setmode(GPIO.BCM)  # Configurer la numérotation des broches en BCM
GPIO.setwarnings(False)

GPIO.setup(led, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)


def allumer_buzzer():
    while True : 
        GPIO.output(led, GPIO.HIGH)
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led, GPIO.LOW) 
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(1) 

processus_alarme = Process(target=allumer_buzzer)

def alarme(etat):
    global processus_alarme

    print(f"Etat: {etat} {processus_alarme.is_alive()}")
    if etat == 0 and processus_alarme.is_alive():
        processus_alarme.kill()
        processus_alarme = Process(target=allumer_buzzer)
        GPIO.output(led, GPIO.LOW)
        GPIO.output(buzzer, GPIO.LOW)
    elif etat == 1 :
        if not processus_alarme.is_alive():
            processus_alarme.start()

try:
    while True:
        a = input("Allumer?") == "o"
        alarme(a)
except KeyboardInterrupt:
    processus_alarme.kill()
    processus_alarme = Process(target=allumer_buzzer)
    GPIO.output(led, GPIO.LOW)
    GPIO.output(buzzer, GPIO.LOW)

