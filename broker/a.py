import threading

def a():
    print("dfdsfq")

threading.Timer(5, a).start()