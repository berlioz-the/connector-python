# New Environment
```
$ conda create --name berlioz27 --file specs.txt
$ activate berlioz27                # Windows
$ source activate berlioz27         # Mac
$ pip install -r requirements.txt
```

# Publishing
https://blog.jetbrains.com/pycharm/2017/05/how-to-publish-your-package-on-pypi/

Update Version in berlioz/metadata.py
```
$ python setup.py sdist
$ twine register -r berlioz-prod dist/<THE-TAR-GZ> # FIRST TIME ONLY
$ twine upload -r berlioz-prod dist/<THE-TAR-GZ>
```

# Hacks
## Thrift Windows Issue
https://github.com/eleme/thriftpy/issues/234
```
C:\Users\Ruben\AppData\Local\conda\conda\envs\berlioz27\lib\site-packages\thriftpy\parser\parser.py
line 488: if url_scheme == '' or os.path.exists(path):
```
# Details

## Conda Stuff
```
$ conda install --name berlioz27 --file specs.txt
$ conda list --explicit > specs.txt
```

## POP Stuff
```
$ pip install win_inet_pton
$ pip freeze > requirements.txt
```

## Running on Mac
```
$ source activate berlioz27
$ source deactivate
```

## Running on Windows
(anaconda prompt)
```
$ activate berlioz27
$ deactivate
```

# Documentation

## Python 3 HTTP Client & Server Library
https://aiohttp.readthedocs.io/en/stable/#

## Python 2 vs 3
http://python-future.org/compatible_idioms.html
https://wiki.python.org/moin/Python2orPython3
