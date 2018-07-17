import boto3

def fetchDynamoClient(peer):
    kwargs = _getClientConfig(peer)
    dynamodb = boto3.resource('dynamodb', **kwargs)
    return dynamodb.Table(peer['name'])

def fetchKinesisClient(peer):
    kwargs = _getClientConfig(peer)
    return boto3.client('kinesis', **kwargs)

def fetchSSMClient(peer):
    kwargs = _getClientConfig(peer)
    return boto3.client('ssm', **kwargs)

def setupKinesisArgs(peer, actionName, xargs, xkwargs):
    if actionName == 'get_records':
        return
    if actionName == 'list_shards' and 'NextToken' in xkwargs:
        return
    xkwargs['StreamName'] = peer['name']

def setupParameterArgs(peer, actionName, xargs, xkwargs):
    xkwargs['Name'] = peer['name']

def _getClientConfig(peer):
    kwargs = {}
    peerConfig = peer.get('config')
    if peerConfig:
        region = peerConfig.get('region')
        if region:
            kwargs['region_name'] = region
        credentials = peerConfig.get('credentials')
        if credentials:
            key = credentials.get('accessKeyId')
            if key:
                kwargs['aws_access_key_id'] = key
            secret = credentials.get('secretAccessKey')
            if secret:
                kwargs['aws_secret_access_key'] = secret
    return kwargs