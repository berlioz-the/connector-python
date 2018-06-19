import log
logger = log.get(__name__)

import websocket
import json
from delay import delayed

class Client(): 

    def __init__(self, handler): 
        self._handler = handler
        self.ws = None
        self.isClosed = False
        websocket.enableTrace(True)
        self._connect()

    def close(self):
        self.isClosed = True
        if self.ws is not None:
            self.ws.close()

    def _connect(self):
        if self.ws is not None:
            return
        if self.isClosed:
            return

        logger.info('Connecting...')
        self.ws = websocket.WebSocketApp("ws://127.0.0.1:55555/82d1c32d-19bd-4e8b-a53b-7529e386b7c3",
                                    on_message = self._onMessage,
                                    on_error = self._onError,
                                    on_close = self._onClose)
        self.ws.on_open = self._onOpen
        self.ws.run_forever()

    def _onMessage(self, ws, message):
        if not ws is self.ws:
            return
        logger.info('Message received.')
        logger.debug('Message RAW contents: %s', message)
        data = json.loads(message)
        logger.debug('Message JSON Contents: %s', data)
        self._handler(data)

    def _onError(self, ws, error):
        logger.error('Error')
        logger.error(error)
        ws.close()

    def _onClose(self, ws):
        logger.info('Closed')
        self.ws = None
        self._reconnect()

    def _onOpen(self, ws):
        logger.info('Opened')

    @delayed(1)
    def _reconnect(self):
        self._connect()
