from flask import g as flask_g
from flask import request as flask_request

class Flask:
    def __init__(self, app, zipkin, policy):
        self._app = app
        self._zipkin = zipkin
        self._policy = policy
        
        self._app.before_request(self._handleBeforeRequest)
        self._app.after_request(self._handleAfterRequest)

    def _handleBeforeRequest(self):
        url = ''
        if flask_request.script_root is not None:
           url = flask_request.script_root
        if flask_request.path is not None:
           url = url + flask_request.path
        zipkin_span = self._zipkin.instrumentServer(flask_request.headers,
                                                    flask_request.method,
                                                    url)
        flask_g._berlioz_zipkin_span = zipkin_span
        zipkin_span.start()

    def _handleAfterRequest(self, response):
        zipkin_span = getattr(flask_g, '_berlioz_zipkin_span')
        if zipkin_span:
            self._zipkin.serverResponse(zipkin_span, response.status_code)
        return response