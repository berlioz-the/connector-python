import log
logger = log.get(__name__)

from utils import delay
import os
import websocket
import json
import threading

class Client(): 

    def __init__(self, handler): 
        logger.info('Constructing.')
        self._handler = handler
        self.ws = None
        self.isClosed = False
        websocket.enableTrace(False)
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
        ws = websocket.WebSocketApp(os.environ['BERLIOZ_AGENT_PATH'],
                                    on_message = self._onMessage,
                                    on_error = self._onError,
                                    on_close = self._onClose)
        ws.on_open = self._onOpen
        ws_thread = threading.Thread(target=ws.run_forever)
        ws_thread.daemon = True
        self.ws = ws
        ws_thread.start()

    def _onMessage(self, ws, message):
        if not ws is self.ws:
            return
        logger.info('Message received.')
        logger.debug('Message RAW contents: %s', message)
        data = json.loads(message)
        logger.debug('Message JSON Contents: %s', data)
        self._handler(data)
        logger.info('Message processed.')

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

    def _reconnect(self):
        if self.isClosed:
            return
        delay(1000, self._connect)
