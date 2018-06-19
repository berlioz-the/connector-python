import log
logger = log.get(__name__)

import json

class Registry:
    
    def __init__(self):
        self._sections = {}
        self._subscribers = {}

    def extractRoot(self):
        return self._sections

    def set(self, sectionName, path, value):
        logger.debug('SET. Section: %s, Path: %s, Value: %s', sectionName, path, value)

        section = self._getSection(sectionName)
        pathStr = self._getKey(path)
        # currValue = section[pathStr]
        # if (_.isEqual(currValue, value)) {
        #     return;
        # }
        section[pathStr] = value
        self._notifyToSubscribers(sectionName, path)

    def get(self, sectionName, path):
        section = self._getSection(sectionName)
        pathStr = self._getKey(path)
        return section[pathStr]

    def reset(self, sectionName):
        logger.debug('RESET. Section: %s', sectionName)
        self._sections[sectionName] = {}

    def _getKey(self, path):
        return json.dumps(path)

    def _getSection(self, name):
        if not name in self._sections:
            self._sections[name] = {}
        return self._sections[name]

    def _notifyToSubscribers(self, sectionName, path):
        pass
