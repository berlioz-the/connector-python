import log
logger = log.get(__name__)

import starter as _starter

# PEERS 
def monitorPeers(kind, name, endpoint, cb):
    _starter.registry.subscribe(kind, [name, endpoint], cb)

def getPeers(kind, name, endpoint):
    return _starter.registry.get(kind, [name, endpoint])

def getRandomPeer(kind, name, endpoint):
    peers = getPeers(kind, name, endpoint)
    return _starter.randomFromDict(peers)

def request(kind, name, endpoint):
    return _starter.makeRequest(kind, name, endpoint)

# DATABASES 
def monitorDatabases(name, cb):
    _starter.monitorNatives('database', name, cb)

def getDatabases(name):
    return _starter.getNatives('database', name)

def getDatabase(name):
    return _starter.getNative('database', name)

def getDatabaseClient(name):
    return _starter.getNativeClient('database', name)

# QUEUES 
def monitorQueues(name, cb):
    _starter.monitorNatives('queue', name, cb)

def getQueues(name):
    return _starter.getNatives('queue', name)

def getQueue(name):
    return _starter.getNative('queue', name)

def getQueueClient(name):
    return _starter.getNativeClient('queue', name)
