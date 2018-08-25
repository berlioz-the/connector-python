from . import log
logger = log.get(__name__)

from .http_peer_accessor import HttpPeerAccessor

class Service(HttpPeerAccessor):
    def __init__(self, starter, id, endpoint):
        HttpPeerAccessor.__init__(self, starter, id, endpoint)

