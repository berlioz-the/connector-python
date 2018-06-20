# import requests

# r = requests.get('http://127.0.0.1:50002')
# print(r)
# print(r.status_code)
# print(r.text)

import boto3

def functionWrapper(fn):
    def inner(*args, **kwargs):
        print 'START'
        res = fn(*args, **kwargs)
        print 'END'
        return res
    return inner

class ClassWrapper(object):

    def __init__(self, target):
        print('****** ' + str(target))
        object.__setattr__(self, "_target", target)

    def __getattribute__(self, name):
        print('****** ' + name)
        target = object.__getattribute__(self, "_target")
        origFn = getattr(target, name)
        return functionWrapper(origFn)


def getTable():
    args = ['dynamodb']
    kwargs = {
        'region_name': 'us-east-1'
    }
    dynamodb = boto3.resource(*args, **kwargs)
    table = dynamodb.Table('my-table')
    wrappedTable = ClassWrapper(table)
    return wrappedTable

myTable = getTable()
print('****** ' + str(myTable))

response = myTable.scan()
print (response)