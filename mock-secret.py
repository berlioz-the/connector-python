import os
# os.environ['BERLIOZ_AGENT_PATH'] = "ws://127.0.0.1:55555/82d1c32d-19bd-4e8b-a53b-7529e386b7c3"
os.environ['BERLIOZ_AGENT_PATH'] = "ws://localhost:40000/9a42261e-28ff-4b6d-8259-2815e503b941"
os.environ['BERLIOZ_CLUSTER'] = "kin"
os.environ['BERLIOZ_SERVICE'] = "web"

if __name__ == '__main__':
    import berlioz
else:
    from . import berlioz

def monitorPublicKeys(peers):
    berlioz.logger.info('**** PublicKey: %s', berlioz.getSecretPublicKey('personal'))
berlioz.monitorSecretPublicKey('personal', monitorPublicKeys)

def monitorPrivateKeys(peers):
    berlioz.logger.info('**** PublicKey: %s', berlioz.getSecretPrivateKey('personal'))
berlioz.monitorSecretPrivateKey('personal', monitorPrivateKeys)

import time

from flask import Flask
from flask.json import jsonify

app = Flask(__name__)
berlioz.setupFlask(app)

app.name = 'myawesomeapp'

@app.route('/')
def hello():
    return "Hello World! "

@app.route('/encrypt')
def encrypt():
    return berlioz.getSecretPublicKeyX('personal').encrypt('lalalalala')

@app.route('/encrypt_decrypt')
def encrypt_decrypt():
    encrypted = berlioz.getSecretPublicKeyX('personal').encrypt('lalalalala')
    decrypted = berlioz.getSecretPrivateKeyX('personal').decrypt(encrypted)
    return decrypted


if __name__ == '__main__':
    app.run()
