## Create New Environment
$ conda create --name berlioz27 --file specs.txt

## Refresh Environment
$ conda install --name berlioz27 --file specs.txt

## Extract Environment
conda list --explicit > specs.txt

## Running on Mac
$ source activate berlioz27
$ source deactivate

## Running on Windows
(anaconda prompt)
$ activate berlioz27
$ deactivate


## PIP Packages
pip install websocket-client


## Python 3 HTTP Client & Server Library 
https://aiohttp.readthedocs.io/en/stable/#

## Python 2 vs 3
http://python-future.org/compatible_idioms.html
https://wiki.python.org/moin/Python2orPython3