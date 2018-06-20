import log
logger = log.get(__name__)

class Zipkin:
    
    def __init__(self, policy):
        self._policy = policy

    def addZipkinHeaders(self, request, traceId):
        pass

    def instrument(self, remoteServiceName, method, url):
        pass