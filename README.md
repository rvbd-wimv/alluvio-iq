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
SHA256(getIQsizing)= 8cc2f41fc293df15516e7884c215a85b3e9736a3360aec9f445f4ab88b5f6835
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
SHA256(getIQsizing_win.exe)= 321980f6804bde4f5aa2909f5bade9a3678a4eb19501bebef6873a5ebed9d967
````



## License

Copyright (c) 2022 Riverbed Technology, Inc.

The scripts provided here are licensed under the terms and conditions of the MIT License accompanying the software ("License"). The scripts are distributed "AS IS" as set forth in the License. The script also include certain third party code. All such third party code is also distributed "AS IS" and is licensed by the respective copyright holders under the applicable terms and conditions (including, without limitation, warranty and liability disclaimers) identified in the license notices accompanying the software.
