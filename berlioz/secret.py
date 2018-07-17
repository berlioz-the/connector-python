from . import log
logger = log.get(__name__)

import json
# from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class BaseRSAKeyClient:
    def __init__(self, starter, name):
        self._starter = starter
        self._name = name

    def _getKeyStr(self, kind):
        client = self._starter.getNativeClient(kind, self._name)
        response = client.get_parameter(WithDecryption=True)
        param = response['Parameter']
        return param['Value']

    def _getKey(self, kind):
        keyStr = self._getKeyStr(kind)
        rsakey = RSA.importKey(keyStr)
        rsakey = PKCS1_OAEP.new(rsakey)
        return rsakey

class SecretClient(BaseRSAKeyClient):
    def __init__(self, starter, name):
        BaseRSAKeyClient.__init__(self, starter, name)

    def encrypt(self, data):
        rsakey = self._getKey('secret_public_key')
        encrypted = rsakey.encrypt(data)
        return encrypted.encode('base64')
        
    def decrypt(self, data):
        rsakey = self._getKey('secret_private_key')
        decrypted = rsakey.decrypt(data.decode('base64'))
        return decrypted
