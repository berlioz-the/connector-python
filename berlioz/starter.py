from . import log
logger = log.get(__name__)

logger.info('Starting...')

import sys
import json
import random as rand

from .registry import Registry
from .policy import Policy
from .zipkin import Zipkin
from .processor import Processor
from .client import Client
from .executor import Executor
from .peer_helper import PeerHelper

import copy
import os

berlioz_cluster = os.environ.get('BERLIOZ_CLUSTER')
berlioz_sector = os.environ.get('BERLIOZ_SECTOR')
berlioz_service = os.environ.get('BERLIOZ_SERVICE')


def onMessage(msg):
    for section, data in msg.items():
        # logger.info('Section %s, data: %s', section, data)
        processor.accept(section, data)
    # logger.info('**** REGISTRY: %s', json.dumps(registry.extractRoot(), indent=4, sort_keys=True))




def monitorNatives(kind, name, cb):
    registry.subscribe(kind, [name], cb)

def getNatives(kind, name):
    return registry.get(kind, [name])

def getNative(kind, name):
    peers = getNatives(kind, name)
    return randomFromDict(peers)





def instrument(method, binary_annotations):
    return zipkin.instrument(method, binary_annotations)


def randomFromList(list):
    return rand.choice(list)

def firstFromList(list):
    return list[0]

def randomFromDict(dict):
    if not dict:
        return None
    key = randomFromList(list(dict.keys()))
    return dict[key]

def firstFromDict(dict):
    if not dict:
        return None
    key = firstFromList(list(dict.keys()))
    return dict[key]

def setupFlask(app):
    from .frameworks.b_flask import Flask
    Flask(app, zipkin, policy)


registry = Registry()
peerHelper = PeerHelper(registry)
policy = Policy(registry)
zipkin = Zipkin(peerHelper, policy)
processor = Processor(registry)
client = Client(onMessage)

