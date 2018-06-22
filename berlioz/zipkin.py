import log
logger = log.get(__name__)

import requests
import os
import platform

if platform.system() == 'Windows':
    import win_inet_pton

from py_zipkin.zipkin import zipkin_span
from py_zipkin.zipkin import ZipkinAttrs
from py_zipkin.util import generate_random_64bit_string as zipkin_generate_span
from py_zipkin.stack import ThreadLocalStack as ZipkinThreadLocalStack

class Zipkin:
    
    def __init__(self, policy):
        self._policy = policy
        self._zipkin_context_stack = ZipkinThreadLocalStack()
        self._localName = os.environ['BERLIOZ_CLUSTER'] + '-' + os.environ['BERLIOZ_SERVICE']
        self._sampleRate = 100
        self._policy.monitor('enable-zipkin', [], self._onZipkinEnabledChanged)
        self._policy.monitor('zipkin-endpoint', [], self._onZipkinEndpointChanged)

    def isEnabled(self):
        return self._isEnabled and self._endpoint

    def addZipkinHeaders(self, headers, zipkin_span):
        if not zipkin_span:
            return
        zipkin_attrs = zipkin_span.zipkin_attrs
        headers['X-B3-TraceId'] = zipkin_attrs.trace_id
        headers['X-B3-SpanId'] = zipkin_attrs.span_id
        headers['X-B3-ParentSpanId'] = zipkin_attrs.parent_span_id
        headers['X-B3-Flags'] = zipkin_attrs.flags
        headers['X-B3-Sampled'] = str(int(zipkin_attrs.is_sampled))

    def instrument(self, spanName, binary_annotations=None):
        zipkin_attrs = None
        existing_zipkin_attrs = self._zipkin_context_stack.get()
        if existing_zipkin_attrs:
            zipkin_attrs = ZipkinAttrs(
                span_id = zipkin_generate_span(),
                trace_id = existing_zipkin_attrs.trace_id,
                parent_span_id = existing_zipkin_attrs.span_id,
                flags = existing_zipkin_attrs.flags,
                is_sampled = existing_zipkin_attrs.is_sampled
            )
        return self._instrument(self._localName, spanName, zipkin_attrs, binary_annotations)

    def instrumentRequest(self, remoteServiceName, method, binary_annotations=None):
        zipkin_attrs = None
        existing_zipkin_attrs = self._zipkin_context_stack.get()
        if existing_zipkin_attrs:
            zipkin_attrs = ZipkinAttrs(
                span_id = zipkin_generate_span(),
                trace_id = existing_zipkin_attrs.trace_id,
                parent_span_id = existing_zipkin_attrs.span_id,
                flags = existing_zipkin_attrs.flags,
                is_sampled = existing_zipkin_attrs.is_sampled
            )
        return self._instrument(remoteServiceName, method, zipkin_attrs, binary_annotations)

    def instrumentServer(self, headers, method, url):
        # See https://github.com/openzipkin/zipkin-js/blob/7588d88b876ab5f5844f4bbd08f50c16c13306ab/packages/zipkin/src/instrumentation/httpServer.js
        zipkin_attrs = ZipkinAttrs(
            span_id = headers.get('X-B3-SpanId') or zipkin_generate_span(),
            trace_id = headers.get('X-B3-TraceId') or zipkin_generate_span(),
            parent_span_id = headers.get('X-B3-ParentSpanId'),
            flags = headers.get('X-B3-Flags'),
            is_sampled = str(headers.get('X-B3-Sampled') or '0') == '1'
        )
        binary_annotations = {
            'http.url': url
        }
        return self._instrument(self._localName, method, zipkin_attrs, binary_annotations)

    def serverResponse(self, zipkin_span, status_code):
        zipkin_span.update_binary_annotations({
            'http.status_code': status_code 
        }) 
        zipkin_span.stop()

    def _instrument(self, serviceName, spanName, zipkin_attrs, binary_annotations=None):
        zipArgs = {
            "service_name": serviceName,
            "span_name": spanName,
            "transport_handler": self._zipkin_http_transport,
            "port": 0,
            "sample_rate": self._sampleRate,
            "zipkin_attrs": zipkin_attrs,
            "binary_annotations": binary_annotations
        }
        return zipkin_span(**zipArgs)

    def _zipkin_http_transport(self, encoded_span):
        if not self._isEnabled:
            return
        zipkin_url = self._endpoint
        if not zipkin_url:
            return
        # TODO: check https://github.com/Yelp/py_zipkin#transport for
        # body = b"\x0c\x00\x00\x00\x01" + encoded_span
        headers = {"Content-Type": "application/x-thrift"}
        # TODO: Run in a thread
        try:
            requests.post(zipkin_url, data=encoded_span, headers=headers)
        except Exception, e:
            logger.error(e)

    def _onZipkinEnabledChanged(self, value):
        self._isEnabled = value

    def _onZipkinEndpointChanged(self, value):
        self._endpoint = value
        if self._endpoint:
            self._endpoint = self._endpoint.replace('v2', 'v1')

