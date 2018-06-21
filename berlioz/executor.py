import log
logger = log.get(__name__)

import os
from utils import delay
import random as rand
import time

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
            self._remoteServiceName = os.environ['BERLIOZ_CLUSTER'] + '-' + '-'.join(target)

        self._context = {
            "canRetry": True,
            "tryCount": 0
        }

    def perform(self):
        while self._canTry():
            self._retryWait()
            self._try()
            if self._checkCompleted():
                return self._context['result']
        exInfo = self._context['lastError']
        if exInfo:
            raise exInfo

    def _canTry(self):
        if self._context['tryCount'] == 0:
            return True
        if self._context['tryCount'] >= self._resolvePolicy('retry-count'):
            return False
        return self._context['canRetry']

    def _try(self):
        logger.info('_try begin')

        self._context['hasError'] = False
        self._context['lastError'] = None
        self._context['tryCount'] = self._context['tryCount'] + 1

        self._perform()
        logger.info('_try end')

    def _retryWait(self):
        if self._context['tryCount'] == 0:
            return
        logger.info('_retryWait')

        timeout = self._resolvePolicy('retry-initial-delay')
        timeout = timeout * pow(self._resolvePolicy('retry-delay-multiplier'), self._context['tryCount'] - 1)
        timeout = min(timeout, self._resolvePolicy('retry-max-delay'))
        logger.info('_retryWait timeout: %s', timeout)

        if timeout > 0:
            # tracer = this._instrument('sleep', 'GET', 'http://sleep')
            time.sleep(timeout / 1000)

    def _perform(self):
        try:
            peer = self._fetchPeer()
            if not peer:
                if not self._resolvePolicy('no-peer-retry'):
                    self._context['canRetry'] = False
                raise Exception('No peers found', self._target)

            zipki_span = None
            if self._zipkin:
                binary_annotations = {
                    'http.url': self._trackerUrl
                }
                zipki_span = self._zipkin.instrumentRequest('-'.join(self._target),
                                                            self._trackerMethod,
                                                            binary_annotations)
            if zipki_span:
                with zipki_span:
                    result = self._actionCb(peer, zipki_span)
            else:
                result = self._actionCb(peer)
            logger.debug('Result: %s', result)
            self._context['result'] = result
        except Exception as ex:
            self._context['hasError'] = True
            self._context['lastError'] = ex
            logger.exception('operation failed')

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
        if not peers:
            return None
        key = rand.choice(peers.keys()) 
        return peers[key]

    def _checkCompleted(self):
        if self._context['hasError']:
            return False
        return True

    def _resolvePolicy(self, name):
        return self._policy.resolve(name, self._target)