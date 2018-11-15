from . import log
logger = log.get(__name__)

import requests
import json

from .peer_accessor import PeerAccessor

class HttpPeerAccessor(PeerAccessor):
    def __init__(self, starter, id, endpoint):
        if endpoint is None:
            endpoint = 'default'
        serviceId = id + '-' + endpoint
        PeerAccessor.__init__(self, starter, [serviceId])

    def request(self ):
        return RequestWrapper(self)

class RequestWrapper(object):

    def __init__(self, target):
        object.__setattr__(self, "_target", target)

    def __getattribute__(self, propKey):

        def perform(*args, **kwargs):
            print(args)
            print(kwargs)
            kwargs.setdefault('headers', {})

            target = object.__getattribute__(self, "_target")
            if propKey == 'request':
                method = args[0]
                url = args[1]
            else:
                method = propKey 
                url = args[0]

            def execAction(peer, zipkin_span=None):
                print(peer)
                print(url)
                origMethod = getattr(requests, propKey)
                newargs = []
                if propKey == 'request':
                    newargs.append(method)    
                finalUrl = peer['protocol'] + '://' + peer['address'] + ':' + str(peer['port'])
                if url:
                    finalUrl = finalUrl + url
                newargs.append(finalUrl)
                if zipkin_span:
                    target._starter.zipkin.addZipkinHeaders(kwargs['headers'], zipkin_span)
                result = origMethod(*newargs, **kwargs)
                return result
            binary_annotations = {
                'http.url': url
            }
            return target.performExecutor(method, binary_annotations, execAction)

        return perform

