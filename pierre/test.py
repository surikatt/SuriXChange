import time
import digitalio
import board
import adafruit_matrixkeypad

colonnes = [digitalio.DigitalInOut(x) for x in ( board.D9, board.D6, board.D5 )]
lignes = [digitalio.DigitalInOut(x) for x in ( board.D13, board.D12, board.D11, board.D10 )]

touches = (( 1 , 2 , 3 , 'F'),
           ( 4 , 5 , 6 , 'E'),
           ( 7 , 8 , 9 , 'D'),
           ( 'A' , 0 , 'B' , 'C')
          )

keypad = adafruit_matrixkeypad.Matrix_Keypad(lignes, colonnes, touches)

while True :
     keys = keypad.pressed_keys
     if  keys :
         print ( "Appuyé : " , keys )
     time.sleep(0.1)
     

