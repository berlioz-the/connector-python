from . import log
logger = log.get(__name__)

import json


class Policy:
    
    def __init__(self, registry):
        self._registry = registry
        self._defaults = {
            'enable-zipkin': False,
            'zipkin-endpoint': '',
            'timeout': 5000,
            'no-peer-retry': True,
            'retry-count': 3,
            'retry-initial-delay': 500,
            'retry-delay-multiplier': 2,
            'retry-max-delay': 5000
        }

    def monitor(self, name, target, cb):
        context = {
            "value": self.resolve(name, target),
        }
        cb(context["value"])
        self._registry.subscribe('policies', [], lambda l: self._processMonitor(context, name, target, cb))

    def _processMonitor(self, context, name, target, cb):
        newValue = self.resolve(name, target)
        if context["value"] != newValue:
            context["value"] = newValue
            cb(newValue)

    def resolve(self, name, target):
        root = self._registry.get('policies', [])
        if root is None:
            root = {}
        if target is None:
            target = []

        value = self._resolve(root, name, target)
        if value is not None:
            return value

        value = self._defaults.get(name)
        if value is not None:
            return value
        
        logger.error('No Default set for %s', name)
        return None

    def _resolve(self, root, name, target):
        value = None
        if target:
            children = root.get('children')
            if children:
                child = children.get(target[0])
                if child:
                    childTarget = target[1:]
                    value = self._resolve(child, name, childTarget)
        if value:
            return value
        values = root.get('values')
        if values:
            return values.get(name)
        return None