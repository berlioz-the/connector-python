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