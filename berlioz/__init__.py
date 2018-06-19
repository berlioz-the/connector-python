import log
logger = log.get(__name__)

import starter as _starter

def monitorPeers(kind, name, endpoint, cb):
    logger.info('MonitorPeers. Kind: %s, Service: %s, Endpoint: %s', kind, name, endpoint)
    _starter.registry.subscribe(kind, [name, endpoint], cb)
