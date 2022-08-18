# unisat_data_local (UniSat Data Provider)

#implements: PSoTT Local

## Installing 

### Install Python3 

- Linux
  - ``` sudo apt update && sudo apt upgrade && sudo apt install python3 python3-pip python3-dev python3-venv```
- Mac
  - ``` brew update && brew upgrade && brew install python3``
- Windows
  - Error: Platform Not Supported

### Installing this Package

Download the package (or git clone ) to `/home/pi/<any folder>/` 

Run `python3 -m venv venv`

Run `source venv venv`

Run `python3 -m pip install -U pip setuptools wheel`

Run `pip3 install -r requirements.txt` 

## Configuring the Package

open `config.ini` file with any supported text editor. You need to edit several configuration values, 

DEV_ID :  This unique id should be added as the same value that comes from the serial as devID. 

UART_PORT: This should be the correct port, which receives the serial data.

DEFAULT_SYNCING_INTERVAL : (in seconds) time interval to sync data between devices and cloud. (set this to some larger value such as 300 (5 minute) if local storage is small)

LOG_LEVEL : If anything works not correctly, set log level as `debug`

