import RPi.GPIO as GPIO
import time

# Définir le mode de numérotation des broches (BROADCOM ou BOARD)
GPIO.setmode(GPIO.BCM)

# Définir les broches que nous voulons lire
broches = [27, 22,]

# Configurer les broches en mode entrée
GPIO.setup(2, GPIO.OUT)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)

# Lire l'état des broches et afficher leur état
while True:

    
    if GPIO.input(27) == GPIO.HIGH:
        print("A")
    if GPIO.input(22) == GPIO.HIGH:
        print("B")
    else : print(" ")

    