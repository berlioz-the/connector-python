import threading

def delay(timeout, f):
    t = threading.Timer(timeout / 1000, f)  
    t.start()

def calculateIdentity(envMap):
    identity = envMap.get('BERLIOZ_IDENTITY')

    prefix = envMap.get('BERLIOZ_IDENTITY_PREFIX')
    if prefix:
        if identity.startswith(prefix):
            identity = identity[len(prefix):]

    proc = envMap.get('BERLIOZ_IDENTITY_PROCESS')
    if proc == 'plus_one':
        identity = str(int(identity) + 1)

    return identity