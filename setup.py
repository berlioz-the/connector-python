import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "berlioz",
    version = "0.0.4",
    url = 'https://berlioz.cloud',
    author = "Ruben Hakopian",
    author_email = "ruben@berlioz.cloud",
    description = ("Python SDK for Berlioz Cloud"),
    license = "Apache License 2.0",
    keywords = "microservices service mesh cloud aws",
    packages=['berlioz'],
    long_description=read('README.rst'),
    platforms='any',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
)
