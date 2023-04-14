import time
import digitalio
import board
import adafruit_matrixkeypad

liste_pin_ligne = [digitalio.DigitalInOut(x) for x in ( board.D13, board.D12, board.D11, board.D10 )]
liste_pin_colonne = [digitalio.DigitalInOut(x) for x in ( board.D9, board.D6, board.D5, board.D8 )]

def lire_clavier():
    for pin_ligne in liste_pin_ligne:
        digitalWrite(pin_ligne, HIGH)
        for pin_colonne in liste_pin_colonne:
            if digitalRead(pin_colonne):
                return (pin_ligne, pin_colonne)
        digitalWrite(pin_ligne, LOW)
    return False

while True :
     keys = keypad.pressed_keys
     if  keys :
         print ( "Appuyé : " , keys )
         time.sleep(0.1)
