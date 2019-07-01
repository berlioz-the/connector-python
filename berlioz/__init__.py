from . import log
logger = log.get(__name__)

from . import metadata
logger.info('BerliozPythonSDK v%s', metadata.VERSION)

from . import environment

if not environment.get('BERLIOZ_CLUSTER'):
    logger.warning('Using berlioz sdk outside of managed environment.')
else:
    from . import starter as _starter
    from .secret import SecretClient
    from .cluster import Cluster
    from .sector import Sector

    from functools import wraps
    import inspect

    from .utils import calculateIdentity
    my_identity = calculateIdentity(environment.getMap())

    # IDENTITY
    def identity():
        return my_identity

    # PEERS
    def cluster(name, endpoint=None):
        return Cluster(_starter, name, endpoint)

    def sector(name):
        return Sector(_starter, name)

    def service(name, endpoint=None):
        return sector(_starter.berlioz_sector).service(name, endpoint)

    def database(name):
        return sector(_starter.berlioz_sector).database(name)

    def queue(name):
        return sector(_starter.berlioz_sector).queue(name)


    # # SECRET PUBLIC KEY
    # def monitorSecretPublicKey(name, cb):
    #     _starter.monitorNatives('secret_public_key', name, cb)

    # def getSecretPublicKeys(name):
    #     return _starter.getNatives('secret_public_key', name)

    # def getSecretPublicKey(name):
    #     return _starter.getNative('secret_public_key', name)

    # def getSecretPublicKeyClient(name):
    #     return _starter.getNativeClient('secret_public_key', name)

    # # SECRET PRIVATE KEY
    # def monitorSecretPrivateKey(name, cb):
    #     _starter.monitorNatives('secret_private_key', name, cb)

    # def getSecretPrivateKeys(name):
    #     return _starter.getNatives('secret_private_key', name)

    # def getSecretPrivateKey(name):
    #     return _starter.getNative('secret_private_key', name)

    # def getSecretPrivateKeyClient(name):
    #     return _starter.getNativeClient('secret_private_key', name)

    # # SECRET PUBLIC & PRIVATE KEY
    # def getSecret(name):
    #     return SecretClient(_starter, name)

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