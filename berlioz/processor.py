from . import log
logger = log.get(__name__)

class Processor:
    
    def __init__(self, registry):
        self._registry = registry
        self._messageHandlers = {
            "policies": self._acceptPolicies,
            "endpoints": self._acceptEndpoints,
            "peers": self._acceptPeers
        }
        self._peerHandler = {
            "service": self._handleServicePeers,
            "cluster": self._handleServicePeers,
            "database": self._handleNativePeers,
            "queue": self._handleNativePeers
        }

    def accept(self, section, data):
        logger.debug('Accept Section: %s, data: %s', section, data)

        handler = self._messageHandlers[section]
        if handler is not None: 
            return handler(data)

    def _acceptPolicies(self, data):
        if data is not None:
            self._registry.set('policies', [], data)
        else:
            self._registry.reset('policies')

    def _acceptEndpoints(self, data):
        if data is not None:
            self._registry.set('endpoints', [], data)
            for endpointName, endpoints in data.items():
                self._registry.set('endpoints', [endpointName], endpoints)
        else:
            self._registry.reset('endpoints')

    def _acceptPeers(self, data):
        if data is not None:
            self._registry.set('endpoints', [], data)
            for kind, peers in data.items():
                if kind in self._peerHandler:
                    self._peerHandler[kind](kind, peers)
        else:
            self._registry.reset('service')
            self._registry.reset('cluster')

    def _handleServicePeers(self, kind, data):
        for name, serviceData in data.items():
            for endpoint, endpointData in serviceData.items():
                self._registry.set(kind, [name, endpoint], endpointData)

    def _handleNativePeers(self, kind, data):
        for name, endpointData in data.items():
            self._registry.set(kind, [name], endpointData)
