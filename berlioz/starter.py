import log
logger = log.get(__name__)

import sys
import signal
import json
import random as rand

from registry import Registry
from policy import Policy
from processor import Processor
from client import Client

registry = Registry()
policy = Policy(registry)
processor = Processor(registry)

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


def monitorNatives(kind, name, cb):
    registry.subscribe(kind, [name], cb)

def getNatives(kind, name):
    return registry.get(kind, [name])

def getNative(kind, name):
    peers = getNatives(kind, name)
    return randomFromDict(peers)



def randomFromList(list):
    return rand.choice(list)

def randomFromDict(dict):
    if not dict:
        return False
    key = randomFromList(dict.keys())
    return dict[key]
