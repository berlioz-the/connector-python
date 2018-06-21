import log
logger = log.get(__name__)

logger.info('Starting...')

import sys
import json
import random as rand

from registry import Registry
from policy import Policy
from zipkin import Zipkin
from processor import Processor
from client import Client
from executor import Executor

import copy
import requests

registry = Registry()
policy = Policy(registry)
zipkin = Zipkin(policy)
processor = Processor(registry)

def onMessage(msg):
    for section, data in msg.items():
        # logger.info('Section %s, data: %s', section, data)
        processor.accept(section, data)
    # logger.info('**** REGISTRY: %s', json.dumps(registry.extractRoot(), indent=4, sort_keys=True))
client = Client(onMessage)


def monitorNatives(kind, name, cb):
    registry.subscribe(kind, [name], cb)

def getNatives(kind, name):
    return registry.get(kind, [name])

def getNative(kind, name):
    peers = getNatives(kind, name)
    return randomFromDict(peers)



def makeRequest(kind, name, endpoint):
    return RequestWrapper([kind, name, endpoint])

class RequestWrapper(object):

    def __init__(self, target):
        object.__setattr__(self, "_target", target)

    def __getattribute__(self, propKey):

        def perform(*args, **kwargs):
            print(args)
            print(kwargs)
            target = object.__getattribute__(self, "_target")
            if propKey == 'request':
                method = args[0]
                url = args[1]
            else:
                method = propKey 
                url = args[0]

            def execAction(peer):
                print(peer)
                print(url)
                origMethod = getattr(requests, propKey)
                newargs = []
                if propKey == 'request':
                    newargs.append(method)    
                newargs.append(peer['protocol'] + '://' + peer['address'] + ':' + str(peer['port']) + url)
                result = origMethod(*newargs, **kwargs)
                return result
            executor = Executor(registry, policy, zipkin, target, method, url, execAction)
            return executor.perform()

        return perform


import aws as AWS
nativeClientFetcher = {
    "dynamodb" : AWS.fetchDynamoClient,
    "kinesis" : AWS.fetchKinesisClient
}
nativeClientArgSetter = {
    "kinesis" : AWS.setupKinesisArgs
}


class NativeResourceWrapper(object):

    def __init__(self, target):
        object.__setattr__(self, "_target", target)

    def __getattribute__(self, propKey):

        def perform(*args, **kwargs):
            target = object.__getattribute__(self, "_target")

            def execAction(peer):
                logger.info('Running %s', propKey)
                clientFetcher = nativeClientFetcher.get(peer['subClass'])
                if not clientFetcher:
                    raise Exception('Service not supported', peer['subClass'])
                client = clientFetcher(peer)
                origMethod = getattr(client, propKey)
                argsSetter = nativeClientArgSetter.get(peer['subClass'])
                if argsSetter:
                    argsSetter(peer, propKey, args, kwargs)
                result = origMethod(*args, **kwargs)
                logger.info('Running %s completed', propKey)
                return result
            executor = Executor(registry, policy, zipkin, target, propKey, '/', execAction)
            return executor.perform()

        return perform


def getNativeClient(kind, name):
    nativeClient = NativeResourceWrapper([kind, name])
    return nativeClient


def randomFromList(list):
    return rand.choice(list)

def randomFromDict(dict):
    if not dict:
        return False
    key = randomFromList(dict.keys())
    return dict[key]
