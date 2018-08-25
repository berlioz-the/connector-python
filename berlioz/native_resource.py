from . import log
logger = log.get(__name__)

from .peer_accessor import PeerAccessor


from . import aws as AWS
nativeClientFetcher = {
    "dynamodb" : AWS.fetchDynamoClient,
    "kinesis" : AWS.fetchKinesisClient,
    "rsa-secret" : AWS.fetchSSMClient
}
nativeClientArgSetter = {
    "kinesis" : AWS.setupKinesisArgs,
    "rsa-secret" : AWS.setupParameterArgs
}

class NativeResource(PeerAccessor):
    def __init__(self, starter, id, endpoint):
        if endpoint is None:
            endpoint = 'default'
        PeerAccessor.__init__(self, starter, [id, endpoint])

    def client(self):
        nativeClient = NativeResourceWrapper(self)
        return nativeClient

class NativeResourceWrapper(object):

    def __init__(self, target):
        object.__setattr__(self, "_target", target)

    def __getattribute__(self, propKey):

        def perform(*args, **kwargs):
            target = object.__getattribute__(self, "_target")

            def execAction(peer, zipkin_span=None):
                logger.info('Running %s', propKey)
                clientFetcher = nativeClientFetcher.get(peer['subClass'])
                if not clientFetcher:
                    raise Exception('Service not supported', peer['subClass'])
                client = clientFetcher(peer)
                origMethod = getattr(client, propKey)
                argsSetter = nativeClientArgSetter.get(peer['subClass'])
                if argsSetter:
                    argsSetter(peer, propKey, args, kwargs)
                logger.info('Args: %s ', args)
                logger.info('kwargs: %s ', kwargs)
                result = origMethod(*args, **kwargs)
                logger.info('Running %s completed', propKey)
                return result

            return target.performExecutor(propKey, None, execAction)

        return perform
