import os
# os.environ['BERLIOZ_AGENT_PATH'] = "ws://127.0.0.1:55555/82d1c32d-19bd-4e8b-a53b-7529e386b7c3"
os.environ['BERLIOZ_AGENT_PATH'] = "ws://172.17.0.2:55555/c3982ad5-0f0f-4451-a7fa-898667106784"
os.environ['BERLIOZ_CLUSTER'] = "kin"

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

import win_inet_pton
from py_zipkin.zipkin import zipkin_span
import requests

from flask_zipkin import Zipkin

zipkin = Zipkin(sample_rate=100)
zipkin.init_app(app)

@zipkin.transport_handler
def http_transport(encoded_span):
    print('88888888888888888888888888888')
    # encoding prefix explained in https://github.com/Yelp/py_zipkin#transport 
    body = b"\x0c\x00\x00\x00\x01" + encoded_span
    print(encoded_span)
    zipkin_url = "http://172.17.0.3:9411/api/v1/spans"
    headers = {"Content-Type": "application/x-thrift"}

    # You'd probably want to wrap this in a try/except in case POSTing fails
    res = requests.post(zipkin_url, data=encoded_span, headers=headers)
    print(res)
    print(res.text)

@zipkin.transport_exception_handler
def default_ex_handler(self, ex):
    raise ex



@app.route('/')
def hello():
    kwargs = {
        # name of the service, app, or otherwise overall component
        "service_name": "myawesomeapp",
        # name of the individual trace point, e.g. function name itself
        "span_name": "index",
        # must define a transport handler like above (or one for Kafka or Scribe)
        "transport_handler": http_transport,
        # the port (int) on which your service/app/component runs
        "port": 1234,
        # Sample rate (int) from 0 to 100; use 100 to always trace
        "sample_rate": 100
    }
    with zipkin_span(**kwargs):
        time.sleep(1)
        some_other_func()
        time.sleep(1)
    return "Hello World!"

@app.route('/kuku')
def kuku():
    return "kuku"

@zipkin_span(service_name="myawesomeapp", span_name="some_other_func")
def some_other_func():
    time.sleep(1)

if __name__ == '__main__':
    app.run()
