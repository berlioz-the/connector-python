from flask import Flask
import berlioz


berlioz.monitorPeers('service', 'app', 'client', lambda x: berlioz.logger.info(x))

import threading

def output():
    threading.Timer(5.0, output).start()
    print '*******************************'
    berlioz.logger.info('Peers: %s', berlioz.getPeers('service', 'app', 'client'))
    berlioz.logger.info('RandomPeer: %s', berlioz.getRandomPeer('service', 'app', 'client'))
    berlioz.logger.info('Database: %s', berlioz.getDatabase('drugs'))
    berlioz.logger.info('Queue: %s', berlioz.getQueue('jobs'))

output()

# logger = berlioz.log.get('berlioz')
# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hello World!"

# if __name__ == '__main__':
#     app.run()
