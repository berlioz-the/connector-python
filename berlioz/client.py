import websocket
import json
from delay import delayed

class Client(): 

    def __init__(self): 
        websocket.enableTrace(True)
        self.ws = None
        self.isClosed = False
        self.connect()

    def on_message(self, ws, message):
        if not ws is self.ws:
            return
        # print message
        data = json.loads(message)
        print("### message ###")
        print(json.dumps(data, indent=4, sort_keys=True))

    def on_error(self, ws, error):
        print(error)
        ws.close()

    def on_close(self, ws):
        print("### closed ###")
        self.ws = None
        self.reconnect()

    def on_open(self, ws):
        print("### opened ###")

    def connect(self):
        if self.ws is not None:
            return
        if self.isClosed:
            return

        print 'Trying to connect....'
        self.ws = websocket.WebSocketApp("ws://127.0.0.1:55555/82d1c32d-19bd-4e8b-a53b-7529e386b7c3",
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def close(self):
        self.isClosed = True
        if self.ws is not None:
            self.ws.close()

    @delayed(1)
    def reconnect(self):
        self.connect()
