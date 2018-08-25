from . import log
logger = log.get(__name__)

from .http_peer_accessor import HttpPeerAccessor

class Cluster(HttpPeerAccessor):
    def __init__(self, starter, name, endpoint):
        id = 'cluster://' + name
        HttpPeerAccessor.__init__(self, starter, id, endpoint)

