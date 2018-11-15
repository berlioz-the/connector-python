from . import log
logger = log.get(__name__)

class Processor:
    
    def __init__(self, registry):
        self._registry = registry
        self._messageHandlers = {
            "policies": self._acceptPolicies,
            "endpoints": self._acceptEndpoints,
            "peers": self._acceptPeers,
            "consumes": self._acceptMetaConsumes
        }

    def accept(self, section, data):
        logger.debug('Accept Section: %s, data: %s', section, data)

        handler = self._messageHandlers.get(section)
        if handler is not None: 
            return handler(data)

    def _acceptPolicies(self, data):
        if data is not None:
            self._registry.set('policies', [], data)
        else:
            self._registry.reset('policies')

    def _acceptMetaConsumes(self, data):
        if data is not None:
            self._registry.set('consumes', [], data)
        else:
            self._registry.reset('consumes')

    def _acceptEndpoints(self, data):
        if data is not None:
            self._registry.set('endpoints', [], data)
            for endpointName, endpoints in data.items():
                self._registry.set('endpoints', [endpointName], endpoints)
        else:
            self._registry.reset('endpoints')

    def _acceptPeers(self, data):
        if data is None:
            self._registry.reset('peers')
        else:
            self._registry.set('peers', [], data)
            for serviceId, serviceData in data.items():
                self._handlePeers(serviceId, serviceData)
            
    def _handlePeers(self, serviceId, serviceData):
        self._registry.set('peers', [serviceId], serviceData)
