# Riverbed Alluvio IQ estimator command line tool

This command line tool can be used to estimate the Alluvio IQ metric packs


## Building MacOS binary

The python script [getspecs.py](getspecs.py) has been compiled with [PyInstaller ](https://pyinstaller.org/en/stable/) with all dependencies included.
````
#pyinstaller --onefile \
--hidden-import socket --hidden-import argparse --hidden-import sys --hidden-import warnings \
--hidden-import logging --hidden-import math --hidden-import steelscript --hidden-import steelscript.netprofiler --hidden-import rich \
--hidden-import requests --hidden-import urllib3 --name getIQsizing \
--paths /Users/devuser/PythonProjects/alluvio-iq/venv/lib/python3.9/site-packages \
getspecs.py
````
## MacOS binary sha256sum
For security purposes, please verify the checksum before running the downloaded [binary](getIQsizing)
````
#openssl sha256 getIQsizing 
SHA256(getIQsizing)= 007cdec540c0b2c5da76885e18949c6c7a9e45573f62ed73e9394818deeb2a9a
````

## Building Windows binary

The python script [getspecs.py](getspecs.py) has been compiled with [PyInstaller ](https://pyinstaller.org/en/stable/) with all dependencies included.
````
#pyinstaller --onefile \
--hidden-import socket --hidden-import argparse --hidden-import sys --hidden-import warnings \
--hidden-import logging --hidden-import math --hidden-import steelscript --hidden-import steelscript.netprofiler --hidden-import rich \
--hidden-import requests --hidden-import urllib3 \
--paths C:\Users\administrator\PythonProjects\alluvio-iq\venv\Lib\site-packages --name getIQsizing_win \
getspecs.py
````
## Windows binary sha256sum
For security purposes, please verify the checksum before running the downloaded [binary](getIQsizing_win.exe)
````
#openssl sha256 getIQsizing_win.exe
SHA256(getIQsizing_win.exe)= 4fbf30e503a751a718add1364904f69c4f74775d6bd397301561d52a9c2bfe28
````



## License

Copyright (c) 2022 Riverbed Technology, Inc.

The scripts provided here are licensed under the terms and conditions of the MIT License accompanying the software ("License"). The scripts are distributed "AS IS" as set forth in the License. The script also include certain third party code. All such third party code is also distributed "AS IS" and is licensed by the respective copyright holders under the applicable terms and conditions (including, without limitation, warranty and liability disclaimers) identified in the license notices accompanying the software.
