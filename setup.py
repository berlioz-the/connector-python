import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "berlioz",
    version = '0.1.2',
    url = 'https://berlioz.cloud',
    author = "Berlioz",
    author_email = "info@berlioz.cloud",
    maintainer = "Ruben Hakopian",
    maintainer_email = "ruben@berlioz.cloud",
    description = ("Python SDK for Berlioz Cloud"),
    license = "Apache License 2.0",
    keywords = "microservices service mesh cloud aws",
    packages=['berlioz', 'berlioz/frameworks'],
    include_package_data=True,
    long_description=read('README.rst'),
    python_requires='>=2.7, >=3.6',
    install_requires=[
        'boto3>=1.7.41',
        'requests>=2.19.1',
        'websocket-client>=0.48.0',
        'py_zipkin>=0.12.0'
    ],
    platforms='any',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring"
    ],
)
