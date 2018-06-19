import log
logger = log.get('berlioz')

from registry import Registry
from client import Client
from processor import Processor
import sys
import signal
import json

registry = Registry()
processor = Processor(registry)

def onMessage(msg):
    for section, data in msg.items():
        # logger.info('Section %s, data: %s', section, data)
        processor.accept(section, data)
    logger.info('**** REGISTRY: %s', json.dumps(registry.extractRoot(), indent=4, sort_keys=True))
client = Client(onMessage)





original_sigint = None

def signalHandler(a,b):
    global original_sigint
    signal.signal(signal.SIGINT, original_sigint)

    print 'EXITING...'
    client.close()
    sys.exit(0)

original_sigint = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGINT,signalHandler)



