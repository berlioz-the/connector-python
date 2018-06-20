import log
logger = log.get(__name__)

import os
from utils import delay
import random as rand

class Executor:
    
    def __init__(self, registry, policy, zipkin, target, trackerMethod, trackerUrl, actionCb):
        self._registry = registry
        self._policy = policy
        self._target = target
        self._trackerMethod = trackerMethod
        self._trackerUrl = trackerUrl
        self._actionCb = actionCb
    
        if self._resolvePolicy('enable-zipkin'):
            logger.info('Zipkin is enabled.')
            self._zipkin = zipkin

        if target[0] == 'service':
            self._remoteServiceName = os.environ['BERLIOZ_CLUSTER'] + '-' + target[1]
        elif target[0] == 'cluster':
            self._remoteServiceName = target[1] + '-' + target[2]
        else:
            self._remoteServiceName = os.environ['BERLIOZ_CLUSTER'] + '-' + target.join('-')

        self._context = {
            "canRetry": True,
            "tryCount": 0
        }

    def perform(self):
        return self._try()

    def _try(self):
        self._context['hasError'] = False
        self._context['lastError'] = None
        self._context['tryCount'] = self._context['tryCount'] + 1

        self._perform()
        if self._checkCompleted():
            return self._context['result']
        else:
            return self._retry()

    def _retry(self):
        if self._context['tryCount'] >= self._resolvePolicy('retry-count'):
            self._context['canRetry'] = False

        if not self._context['canRetry']:
            return self._context['lastError'] #Promise.reject(this._context.lastError);

        return self._retryWait()

    def _retryWait(self):
        # timeout = self._resolvePolicy('retry-initial-delay')
        # timeout = timeout * pow(self._resolvePolicy('retry-delay-multiplier'), self._context['tryCount'] - 1)
        # timeout = min(timeout, self._resolvePolicy('retry-max-delay'))
        # if timeout > 0:
        #     tracer = this._instrument('sleep', 'GET', 'http://sleep')
        #     delay(timeout, self.try, tracer)
        # else:
        #     self.try()
        return self._try()

    def _perform(self):
        peer = self._fetchPeer()
        if not peer:
            if not self._resolvePolicy('no-peer-retry'):
                self._context['canRetry'] = False
            return 'No peer Found' # Promise.reject(new Error('No peer found.'));

        result = self._actionCb(peer) #, tracer.traceId)
        self._context['result'] = result
        return result
        # var tracer = this._instrument(this._remoteServiceName, this._trackerMethod, this._trackerUrl);
        # return Promise.resolve()
        #     .then(result => {
        #         tracer.finish(200);
        #         this._context.result = result;
        #     })
        #     .catch(reason => {
        #         tracer.error(reason);
        #         this._context.hasError = true;
        #         this._context.lastError = reason;
        #         this._logger.error('Executor::_perform::catch: ', reason);
        #     });
    
    def _fetchPeer(self):
        peers = self._registry.get(self._target[0], self._target[1:])
        key = rand.choice(peers.keys()) 
        return peers[key]

    def _checkCompleted(self):
        if self._context['hasError']:
            return False
        return True


    def _resolvePolicy(self, name):
        return self._policy.resolve(name, self._target)