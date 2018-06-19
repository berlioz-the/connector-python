import registry
from client import Client
import sys
import signal

client = Client()

original_sigint = None

def signalHandler(a,b):
    global original_sigint
    signal.signal(signal.SIGINT, original_sigint)

    print 'EXITING...'
    client.close()
    sys.exit(0)

original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT,signalHandler)

kuku = 1234



