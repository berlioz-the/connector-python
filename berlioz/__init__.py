from . import log
logger = log.get(__name__)

from . import metadata
logger.info('BerliozPythonSDK v%s', metadata.VERSION)

import os
if not os.environ.get('BERLIOZ_CLUSTER'):
    logger.warning('Using berlioz sdk outside of managed environment.')
else:
    from . import starter as _starter
    from functools import wraps
    import inspect

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

    # TRACING
    def instrument(method, binary_annotations=None):
        return _starter.instrument(method, binary_annotations)

    def instrument_func(**instArgs):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                mod = inspect.getmodule(f)
                binary_annotations = instArgs.get('binary_annotations', {})
                binary_annotations['source.path'] = mod.__file__
                binary_annotations['source.func'] = f.__name__
                binary_annotations['source.module'] = mod.__name__
                method = instArgs.get('name')
                if not method:
                    method = 'func-' + f.__name__

                with instrument(method, binary_annotations):
                    return f(*args, **kwargs)
            return wrapper
        return decorator

    # FRAMEWORKS
    def setupFlask(app):
        return _starter.setupFlask(app)