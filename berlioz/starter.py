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
from . import environment

import copy


berlioz_cluster = environment.get('BERLIOZ_CLUSTER')
berlioz_sector = environment.get('BERLIOZ_SECTOR')
berlioz_service = environment.get('BERLIOZ_SERVICE')


def onMessage(msg):
    for section, data in msg.items():
        # logger.info('Section %s, data: %s', section, data)
        processor.accept(section, data)
    # logger.info('**** REGISTRY: %s', json.dumps(registry.extractRoot(), indent=4, sort_keys=True))


def instrument(method, binary_annotations):
    return zipkin.instrument(method, binary_annotations)


def setupFlask(app):
    from .frameworks.b_flask import Flask
    Flask(app, zipkin, policy, registry)


registry = Registry()
peerHelper = PeerHelper(registry)
policy = Policy(registry)
zipkin = Zipkin(peerHelper, policy)
processor = Processor(registry)
client = Client(onMessage)

