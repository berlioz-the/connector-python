import log
logger = log.get('berlioz')

import sys
import signal
import json

from registry import Registry
from policy import Policy
from processor import Processor
from client import Client

registry = Registry()
policy = Policy(registry)
processor = Processor(registry)

def onChange(data):
    logger.info('**** ON CHANGE: %s', data)

policy.monitor('zipkin-endpoint', [], onChange)

def onMessage(msg):
    for section, data in msg.items():
        # logger.info('Section %s, data: %s', section, data)
        processor.accept(section, data)
    # logger.info('**** REGISTRY: %s', json.dumps(registry.extractRoot(), indent=4, sort_keys=True))
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



