from . import log
logger = log.get(__name__)

from .service import Service
from .native_resource import NativeResource

class Sector:
    def __init__(self, starter, name):
        self._starter = starter
        self._name = name

    def service(self, name, endpoint):
        id = 'service://' + '-'.join([self._starter.berlioz_cluster, self._name, name])
        return Service(self._starter, id, endpoint)

    def database(self, name):
        return self._nativeResource('database', name)

    def queue(self, name):
        return self._nativeResource('queue', name)

    def _nativeResource(self, kind, name):
        id = kind + '://' + '-'.join([self._starter.berlioz_cluster, self._name, name])
        return NativeResource(self._starter, id)