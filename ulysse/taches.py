from multiprocessing import Process
from time import sleep

def t(prout):
    while True:
        print(prout)
        sleep(1)

patate = Process(target=t, args=["patate"])
spaghetti = Process(target=t, args=["spaghetti"])

patate.start()
spaghetti.start()


