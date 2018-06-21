import os
# os.environ['BERLIOZ_AGENT_PATH'] = "ws://127.0.0.1:55555/82d1c32d-19bd-4e8b-a53b-7529e386b7c3"
os.environ['BERLIOZ_AGENT_PATH'] = "ws://172.17.0.2:55555/9be87152-08fd-480e-9754-f0ec850ee2fc"
os.environ['BERLIOZ_CLUSTER'] = "kin"
os.environ['BERLIOZ_SERVICE'] = "web"

import berlioz


def outputPeers(peers):
    berlioz.logger.info('**** Peers: %s', berlioz.getPeers('service', 'app', 'client'))
    result = berlioz.request('service', 'app', 'client').get('/')
    print('--------------------------------')
    print (result.json())
berlioz.monitorPeers('service', 'app', 'client', outputPeers)

def outputDatabases(peers):
    berlioz.logger.info('**** Database: %s', berlioz.getDatabase('arts'))
    # table = berlioz.getDatabaseClient('arts')
    # contents = table.scan()
    # print('--------------------------------')
    # print (contents)
berlioz.monitorDatabases('arts', outputDatabases)

def outputQueues(peers):
    berlioz.logger.info('*** Queue: %s', berlioz.getQueue('jobs'))
    queue = berlioz.getQueueClient('jobs')
    # result = queue.put_record(
    #     Data='abcd-1234',
    #     PartitionKey='111'
    # )
    # print('--------------------------------')
    # print(result)
    shards = queue.list_shards()
    print('--------------------------------')
    print(shards)
    shardId = shards['Shards'][0]['ShardId']
    iter = queue.get_shard_iterator(ShardId=shardId, ShardIteratorType='TRIM_HORIZON')
    print('--------------------------------')
    print(iter)
    records = queue.get_records(ShardIterator=iter['ShardIterator'])
    print('--------------------------------')
    print(records)
berlioz.monitorDatabases('arts', outputQueues)

import time

from flask import Flask
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

@app.route('/kuku')
def kuku():
    time.sleep(0.5)
    return "kuku"

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
