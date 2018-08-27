from flask import g as flask_g
from flask import request as flask_request
from flask import Response
from flask import json
import pprint

class Flask:
    def __init__(self, app, zipkin, policy, registry):
        self._app = app
        self._zipkin = zipkin
        self._policy = policy
        self._registry = registry
        
        self._app.before_request(self._handleBeforeRequest)
        self._app.after_request(self._handleAfterRequest)
        
        self._app.add_url_rule('/berlioz', 'berlioz_debug', view_func=self._berlioz_debug)


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

    def _berlioz_debug(self):
        data = pprint.pformat(self._registry.extractRoot())
        html = '<html><body><pre>' + data + '</pre></body></html>'
        return html