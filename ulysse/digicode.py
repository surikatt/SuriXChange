import RPi .GPIO as GPIO
import time

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

     

try:
    while True :
        boutons_appuyes = False
        for y in valeur_verticale:
            GPIO.output(y, GPIO.HIGH)
            for x in valeur_horizontale:
                if GPIO.input(x) == 1 :
                    presse = bouton [valeur_horizontale.index(x)][valeur_verticale.index(y)]  

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
                tentative_en_cours = ""
            else :
                print("code erronné")
                tentative_en_cours = ""
                
except KeyboardInterrupt:
    for y in valeur_verticale:
        GPIO.output(y,GPIO.LOW)
    for x in valeur_horizontale:
        GPIO.remove_event_detect(x)


