import os
# os.environ['BERLIOZ_AGENT_PATH'] = "ws://127.0.0.1:55555/82d1c32d-19bd-4e8b-a53b-7529e386b7c3"
os.environ['BERLIOZ_AGENT_PATH'] = "ws://localhost:40000/4f1a9232-e01e-4fa1-a7e0-ad15991a880c"
os.environ['BERLIOZ_CLUSTER'] = "hello"
os.environ['BERLIOZ_SECTOR'] = "main"
os.environ['BERLIOZ_SERVICE'] = "web"

if __name__ == '__main__':
    import berlioz
else:
    from . import berlioz

def onAllPeersChanged(peers):
    berlioz.logger.info('**** onAllPeersChanged: %s', peers)
    berlioz.logger.info('**** random peer: %s', berlioz.service('app').random())
    berlioz.logger.info('**** first peer: %s', berlioz.service('app').first())
    berlioz.logger.info('**** all peers: %s', berlioz.service('app').all())
    # result = berlioz.request('service', 'app', 'client').get('/')
    # print('--------------------------------')
    # print (result.json())
kuku = berlioz.service('app').monitorAll(onAllPeersChanged)

def onFirstPeerChanged(peer):
    berlioz.logger.info('**** onFirstPeerChanged: %s', peer)
kuku = berlioz.service('app').monitorFirst(onFirstPeerChanged)


# def outputDatabases(peers):
#     berlioz.logger.info('**** Database: %s', berlioz.getDatabase('arts'))
#     # table = berlioz.getDatabaseClient('arts')
#     # contents = table.scan()
#     # print('--------------------------------')
#     # print (contents)
# berlioz.monitorDatabases('arts', outputDatabases)

# def outputQueues(peers):
#     berlioz.logger.info('*** Queue: %s', berlioz.getQueue('jobs'))
#     queue = berlioz.getQueueClient('jobs')
#     # result = queue.put_record(
#     #     Data='abcd-1234',
#     #     PartitionKey='111'
#     # )
#     # print('--------------------------------')
#     # print(result)
#     shards = queue.list_shards()
#     print('--------------------------------')
#     print(shards)
#     shardId = shards['Shards'][0]['ShardId']
#     iter = queue.get_shard_iterator(ShardId=shardId, ShardIteratorType='TRIM_HORIZON')
#     print('--------------------------------')
#     print(iter)
#     records = queue.get_records(ShardIterator=iter['ShardIterator'])
#     print('--------------------------------')
#     print(records)
# berlioz.monitorDatabases('arts', outputQueues)

import time

from flask import Flask
from flask.json import jsonify

app = Flask(__name__)
berlioz.setupFlask(app)

app.name = 'myawesomeapp'

@app.route('/')
def hello():
    res = None
    with berlioz.instrument('theremote', binary_annotations={ 'rrr' : 1234 }):
        # time.sleep(.5)
        res = some_other_func()
        # time.sleep(.5)
    # time.sleep(.5)
    return "Hello World! " + res

@app.route('/db')
def db():
    table = berlioz.getDatabaseClient('contacts')
    contents = table.scan()
    return jsonify(contents)

@berlioz.instrument_func()
def some_other_func():
    # pass
    # time.sleep(1)
    res = berlioz.request('service', 'app', 'client').get('/')
    return res.text



# with berlioz.instrument('xxx', binary_annotations={ 'cccc' : 1234 }):
#     time.sleep(0.5)
#     some_other_func()
#     time.sleep(0.25)



if __name__ == '__main__':
    app.run()
