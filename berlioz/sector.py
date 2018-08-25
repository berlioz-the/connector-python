from . import log
logger = log.get(__name__)

from .service import Service

class Sector:
    def __init__(self, starter, name):
        self._starter = starter
        self._name = name

    def service(self, name, endpoint):
        id = 'service://' + '-'.join([self._starter.berlioz_cluster, self._name, name])
        return Service(self._starter, id, endpoint)