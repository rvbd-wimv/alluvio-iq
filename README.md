# Riverbed Alluvio IQ estimator command line tool

This command line tool can be used to estimate the Alluvio IQ metric packs


## Building MacOS binary

The python script [getspecs.py](getspecs.py) has been compiled with [PyInstaller ](https://pyinstaller.org/en/stable/) with all dependencies included.
````
#pyinstaller --onefile \
--hidden-import socket --hidden-import argparse --hidden-import sys --hidden-import warnings \
--hidden-import logging --hidden-import math --hidden-import steelscript --hidden-import steelscript.netprofiler --hidden-import rich \
--hidden-import requests --hidden-import urllib3 \
--paths /Users/devuser/PythonProjects/alluvio-iq/venv/lib/python3.9/site-packages --runtime-tmpdir $HOME \
getspecs.py
````
## MacOS binary sha256sum
For security purposes, please verify the checksum before running the downloaded [binary](getspecs)
````
#openssl sha256 getspecs 
SHA256(getspecs)= 6602f8a94943e47b51fb5e802d79a385d2f7ab94e73357ed8ed08cf4c29a47ac
````

## Building Windows binary

The python script [getspecs.py](getspecs.py) has been compiled with [PyInstaller ](https://pyinstaller.org/en/stable/) with all dependencies included.
````
#pyinstaller --onefile \
--hidden-import socket --hidden-import argparse --hidden-import sys --hidden-import warnings \
--hidden-import logging --hidden-import math --hidden-import steelscript --hidden-import steelscript.netprofiler --hidden-import rich \
--hidden-import requests --hidden-import urllib3 \
--paths C:\Users\administrator\PythonProjects\alluvio-iq\venv\Lib\site-packages --name getspecs_win \
getspecs.py
````
## Windows binary sha256sum
For security purposes, please verify the checksum before running the downloaded [binary](getspecs_win.exe)
````
#openssl sha256 getspecs_win.exe
SHA256(getspecs_win.exe)= 312dc5854a1b093315f359adba7be5d50290c164502a183abaaea12b4cb1f781
````



## License

Copyright (c) 2022 Riverbed Technology, Inc.

The scripts provided here are licensed under the terms and conditions of the MIT License accompanying the software ("License"). The scripts are distributed "AS IS" as set forth in the License. The script also include certain third party code. All such third party code is also distributed "AS IS" and is licensed by the respective copyright holders under the applicable terms and conditions (including, without limitation, warranty and liability disclaimers) identified in the license notices accompanying the software.
