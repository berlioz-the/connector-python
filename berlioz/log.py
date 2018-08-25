import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)

def get(name):
    logger = logging.getLogger(name)
    logger.info("Logger Init")
    return logger