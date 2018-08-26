from . import log
logger = log.get(__name__)

from .deep_eq import deep_eq
import random as rand

class PeerHelper:
    def __init__(self, registry):
        self._registry = registry

    def monitorPeers(self, peerPath, cb):
        self._registry.subscribe('peer', peerPath, cb)

    def monitorPeer(self, peerPath, selector, cb):
        class nonlocal:
            oldValue = None
        
        def innerCb(peers):
            value = selector(peers)
            isChanged = False
            if value is not None:
                if nonlocal.oldValue is not None:
                    isChanged = not deep_eq(value, nonlocal.oldValue)
                else:
                    isChanged = True
            else:
                if nonlocal.oldValue is not None:
                    isChanged = True
                else:
                    isChanged = False
            if isChanged:
                nonlocal.oldValue = value
                cb(value)

        self._registry.subscribe('peer', peerPath, innerCb)

    def getPeers(self, peerPath):
        return self._registry.get('peer', peerPath)

    def getPeer(self, peerPath, selector):
        peers = self._registry.get('peer', peerPath)
        return selector(peers)

    def selectFirstPeer(self, peers):
        return firstFromDict(peers)

    def selectRandomPeer(self, peers):
        return randomFromDict(peers)




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