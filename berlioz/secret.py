from . import log
logger = log.get(__name__)

import json
# from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class BaseRSAKeyClient:
    def __init__(self, kind, starter, name):
        self._kind = kind
        self._starter = starter
        self._name = name

    def _getKeyStr(self):
        client = self._starter.getNativeClient(self._kind, self._name)
        response = client.get_parameter(WithDecryption=True)
        param = response['Parameter']
        return param['Value']

    def _getKey(self):
        keyStr = self._getKeyStr()
        rsakey = RSA.importKey(keyStr)
        rsakey = PKCS1_OAEP.new(rsakey)
        return rsakey

class SecretPublicKeyClient(BaseRSAKeyClient):
    def __init__(self, starter, name):
        BaseRSAKeyClient.__init__(self, 'secret_public_key', starter, name)

    def encrypt(self, data):
        rsakey = self._getKey()
        encrypted = rsakey.encrypt(data)
        return encrypted.encode('base64')
        
class SecretPrivateKeyClient(BaseRSAKeyClient):
    def __init__(self, starter, name):
        BaseRSAKeyClient.__init__(self, 'secret_private_key', starter, name)

    def decrypt(self, data):
        rsakey = self._getKey()
        decrypted = rsakey.decrypt(data.decode('base64'))
        return decrypted
