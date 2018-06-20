import threading

def delay(timeout, f):
    t = threading.Timer(timeout / 1000, f)  
    t.start()