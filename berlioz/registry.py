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
        # currValue = section.get(pathStr)
        # if (_.isEqual(currValue, value)) {
        #     return;
        # }
        section[pathStr] = value
        self._notifyToSubscribers(sectionName, path)

    def get(self, sectionName, path):
        section = self._getSection(sectionName)
        pathStr = self._getKey(path)
        return section.get(pathStr)

    def reset(self, sectionName):
        logger.debug('RESET. Section: %s', sectionName)
        self._sections[sectionName] = {}

    def subscribe(self, sectionName, path, cb):
        subscriberId = self._getSubscriberId(sectionName, path)
        if not subscriberId in self._subscribers:
            self._subscribers[subscriberId] = []
        self._subscribers[subscriberId].append(cb)
        self._notifyToSubscriber(sectionName, path, cb)

    def _getKey(self, path):
        return json.dumps(path)

    def _getSection(self, name):
        if not name in self._sections:
            self._sections[name] = {}
        return self._sections[name]

    def _notifyToSubscribers(self, sectionName, path):
        subscriberId = self._getSubscriberId(sectionName, path)
        if not subscriberId in self._subscribers:
            return
        value = self.get(sectionName, path)
        if not value:
            return
        for cb in self._subscribers[subscriberId]:
            self._triggerToSubscriber(value, cb)

    def _notifyToSubscriber(self, sectionName, path, cb):
        value = self.get(sectionName, path)
        if not value:
            return
        self._triggerToSubscriber(value, cb)

    def _triggerToSubscriber(self, value, cb):
        cb(value)

    def _getSubscriberId(self, sectionName, path):
        subscriber = {
            "section": sectionName,
            "path": path
        }
        return json.dumps(subscriber)
