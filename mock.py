import os
# os.environ['BERLIOZ_AGENT_PATH'] = "ws://127.0.0.1:55555/82d1c32d-19bd-4e8b-a53b-7529e386b7c3"
os.environ['BERLIOZ_AGENT_PATH'] = "ws://127.0.0.1:40000/48b7842a-e61f-409d-8c81-8b2732db28d7"
os.environ['BERLIOZ_CLUSTER'] = "kin"

import berlioz


def outputPeers(peers):
    berlioz.logger.info('**** Peers: %s', berlioz.getPeers('service', 'app', 'client'))
berlioz.monitorPeers('service', 'app', 'client', outputPeers)

def outputDatabases(peers):
    berlioz.logger.info('**** Database: %s', berlioz.getDatabase('arts'))
    table = berlioz.getDatabaseClient('arts')
    contents = table.scan()
    print('--------------------------------')
    print (contents)
berlioz.monitorDatabases('arts', outputDatabases)

def outputQueues(peers):
    berlioz.logger.info('*** Queue: %s', berlioz.getQueue('jobs'))
berlioz.monitorDatabases('arts', outputQueues)




from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
