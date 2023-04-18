import RPi .GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings (False) 

code = "1234A"
tentative_en_cours = ""
bouton = [
    ["1","2","3","F"],
    ["4","5","6","E"],
    ["7","8","9","D"],
    ["A","0","B","C"],]
valeur_verticale = [4,17,27,22]
valeur_horizontale = [5,6,13,26]

for y in valeur_verticale:
    GPIO.setup(y,GPIO.OUT)
    GPIO.setup(y,GPIO.LOW)
for x in valeur_horizontale:
    GPIO.setup(x, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

led_vert = 21
led_jaune = 20
led_rouge = 16

GPIO.setup(led_vert, GPIO.OUT)
GPIO.setup(led_jaune, GPIO.OUT)
GPIO.setup(led_rouge, GPIO.OUT)

def eteindre_vert():
    GPIO.output(led_vert, GPIO.LOW)
    pass
def eteindre_jaune():
    GPIO.output(led_jaune, GPIO.LOW)
    pass
def eteindre_rouge():
    GPIO.output(led_rouge, GPIO.LOW)
    pass



try:
    while True :
        boutons_appuyes = False
        for y in valeur_verticale:
            GPIO.output(y, GPIO.HIGH)
            for x in valeur_horizontale:
                if GPIO.input(x) == 1 :
                    presse = bouton [valeur_horizontale.index(x)][valeur_verticale.index(y)]
                    GPIO.output(led_jaune, GPIO.HIGH)
                    jaune = threading.Timer(0.2, eteindre_jaune).start()
                    

                    if len(tentative_en_cours) < len(code):
                        derniere_touche = presse
                        tentative_en_cours += presse
                        print(tentative_en_cours) 

                        while GPIO.input(x) == 1:
                            pass 

                        time.sleep(0.1)                                         
            GPIO.output(y,GPIO.LOW)

        if len(tentative_en_cours) == len(code):
            if tentative_en_cours == code :
                print("code validé")
                GPIO.output(led_vert, GPIO.HIGH)
                vert = threading.Timer(2, eteindre_vert).start()
                tentative_en_cours = ""
            else :
                print("code erronné")
                GPIO.output(led_rouge, GPIO.HIGH)
                rouge = threading.Timer(2, eteindre_rouge).start()
                tentative_en_cours = ""
                
except KeyboardInterrupt:
    for y in valeur_verticale:
        GPIO.output(y,GPIO.LOW)
    for x in valeur_horizontale:
        GPIO.remove_event_detect(x)
    GPIO.setup(led_vert, GPIO.LOW)
    GPIO.setup(led_jaune, GPIO.LOW)
    GPIO.setup(led_rouge, GPIO.LOW)

