from . import log
logger = log.get(__name__)

from .executor import Executor

class PeerAccessor:
    def __init__(self, starter, peerPath):
        self._starter = starter
        self._peerHelper = self._starter.peerHelper
        self._peerPath = peerPath

    @property
    def peerPath(self):
        return self._peerPath

    @property
    def registry(self):
        return self._starter.registry
    
    def monitorAll(self, cb):
        return self._peerHelper.monitorPeers(self.peerPath, cb)

    def monitorFirst(self, cb):
        return self._peerHelper.monitorPeer(self.peerPath, self._peerHelper.selectFirstPeer, cb)

    def all(self):
        return self._peerHelper.getPeers(self.peerPath)

    def first(self):
        return self._peerHelper.getPeer(self.peerPath, self._peerHelper.selectFirstPeer)

    def random(self):
        return self._peerHelper.getPeer(self.peerPath, self._peerHelper.selectRandomPeer)

    def performExecutor(self, trackerMethod, binary_annotations, actionCb):
        executor = Executor(self, self._starter.policy, self._starter.zipkin, self.peerPath, trackerMethod, binary_annotations, actionCb)
        return executor.perform()