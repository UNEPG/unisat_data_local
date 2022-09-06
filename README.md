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

Run `source venv/bin/activate`

Run `python3 -m pip install -U pip setuptools wheel`

Run `pip3 install -r requirements.txt` 

## Running

### Run Docker Containers

Install docker according to the official docker documentation.

```dockerfile
docker compose up -d
```

### Run data-backend with systemd

Open the `unisat.service` file inside the `system.d` folder, and edit contents

```
[Unit]
Description=UniSat Data Backend Publisher Service for POsTT
After=multi-user.target

[Service]
Type=idle

WorkingDirectory=/home/azat/Developer/test_python_service/python_test
ExecStart=/home/azat/Developer/test_python_service/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

You should at least edit this two lines:

![CleanShot 2022-09-06 at 09.18.36](https://raw.githubusercontent.com/azataiot/images/master/2022/09/upgit_20220906_1662445138.png)

For further info: https://azat.cc/2021/01/18/server-snippets.html#systemd 

## Configuring the Package

open `config.ini` file with any supported text editor. You need to edit several configuration values, 

DEV_ID :  This unique id should be added as the same value that comes from the serial as devID. 

UART_PORT: This should be the correct port, which receives the serial data.

DEFAULT_SYNCING_INTERVAL : (in seconds) time interval to sync data between devices and cloud. (set this to some larger value such as 300 (5 minute) if local storage is small)

LOG_LEVEL : If anything works not correctly, set log level as `debug`

