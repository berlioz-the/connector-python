import logging

def get(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger('berlioz' + name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("Init")

    return logger