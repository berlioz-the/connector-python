from . import log
logger = log.get(__name__)

import os
import re

class Environment: 

    def __init__(self): 
        logger.info('Constructing...')
        self._values = dict()
        for name, value in os.environ.items():
            self._caculateVariable(name, value)

    def get(self, name):
        return self._values.get(name)

    def getMap(self):
        return self._values

    def _caculateVariable(self, name, value):
        groups = re.findall(r"\${(\w*)}", value)
        for g in groups:
            rep = os.environ.get(g)
            value = value.replace("${" + g + "}", rep)
        self._values[name] = value

_env = Environment()

def get(name):
    return _env.get(name)

def getMap():
    return _env.getMap()