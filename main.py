import configparser
import logging
import os
import threading
from pathlib import Path
import time
import kinto_http
import serial
from dotenv import load_dotenv
from kinto_http import KintoException

from src.helpers.objects import dict_without_keys
from src.usart.usart import list_all_available_ports, is_unisat_data_provider

working_dir = Path().absolute()
config_file = working_dir / 'config.ini'

config = configparser.ConfigParser()
config.read(config_file)

# setup logging
logger = logging.getLogger("UniSat Data Provider")
config_log_level = config.get('LOGGING', "LOG_LEVEL", fallback="warning")
if config_log_level.lower() == "debug":
    level = logging.DEBUG
elif config_log_level.lower() == "info":
    level = logging.INFO
elif config_log_level.lower() == "warning":
    level = logging.WARNING
elif config_log_level.lower() == "error":
    level = logging.ERROR
elif config_log_level.lower() == "critical":
    level = logging.CRITICAL
else:
    level = logging.WARNING

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=level)

logger.setLevel(level)

logger.info("Starting UniSat Data Provider...")

logger.info(f"Loaded project configurations as {config.sections()}")


def push_local_data(pkg):
    """create records to the local storage"""
    if not len(pkg) == 0:
        local_client.create_record(bucket="default", collection=dev_id,
                                   data=pkg)


def push_remote_data(pkg):
    if not len(pkg) == 0:
        remote_client.create_record(bucket="default", collection=dev_id,
                                    data=pkg)


def push_data(pkg):
    try:
        push_remote_data(pkg)
    except KintoException as error:
        logger.warning(f"Could not push data to remote_client, exception was {error}")
        push_local_data(pkg)


def handle_data(data):
    global package
    logger.debug("Original data received from serial port: " + str(data))
    data = data.decode('ascii')
    logger.debug("data decoded to string: " + str(data))
    if data == '\r\n':
        timestamp = int(time.time())
        if any(package):
            package['timestamp'] = timestamp
            push_data(package)
        else:
            pass
        # after we pushed that package content, we need to clean up its contents
        package = {}
    else:
        try:
            key, value = data.strip().split("=")  # get the key and value
            # supported data keys for the UniSat data provider.
            if key in ["pressure", "temperature", "humidity", "pm25", "pm10", "lat", "long", "alt"]:
                try:
                    value = float(value)
                except ValueError as er:
                    logger.warning(er)
                    pass
                package[key] = float(value)
        except ValueError as er:
            logger.warning(er)


def sync_data(local_kinto_client, remote_kinto_client, collection_name):
    # retrieve all records from the local kinto client
    local_records = local_kinto_client.get_records(bucket="default", collection=collection_name)
    logger.debug("local_records: %s", local_records)
    for each in local_records:
        data = dict_without_keys(each, ("id", "last_modified"))
        remote_kinto_client.update_record(id=each["id"], data=data, bucket="default", collection=collection_name)
    local_kinto_client.delete_records(bucket="default", collection=collection_name)
    try:
        interval = config.get("SYNCING", "DEFAULT_SYNCING_INTERVAL", fallback=600)
        interval = int(interval)
    except ValueError:
        interval = 600
    # delete null collection
    remote_kinto_client.delete_collection(bucket="default", collection="null", if_exists=True)
    time.sleep(interval)


def read_from_serial(serial_instance):
    global connected
    while not connected:
        connected = True

        while True:
            # new line of data comes from the serial
            reading = serial_instance.readline()  # we got the data line by line
            handle_data(reading)


def get_provider_serial_port():
    """In case that we dot not able to get the serial port value from the configuration file"""
    all_available = list_all_available_ports()
    for each in all_available:
        if is_unisat_data_provider(each):
            return each


if __name__ == '__main__':
    # load env
    load_dotenv()
    logger.info("Loaded environmental variables from .env file")
    # kinto password
    kinto_password = os.getenv('KINTO_PASSWORD')

    dev_id = config.get("DEFAULT", "DEV_ID", fallback="unino")

    try:
        kinto_local_url = config.get("KINTO", "KINTO_LOCAL_URL")
        kinto_remote_url = config.get("KINTO", "KINTO_REMOTE_URL")
    except Exception as e:
        logger.critical(e)
        raise Exception("Could not load project configurations.")

    logger.info(
        f"Get configurations for kinto : dev_id: {dev_id}, "
        f"kinto_local_url: {kinto_local_url}, "
        f"kinto_remote_url: {kinto_remote_url}")

    # initialize the serial connection
    all_ports = list_all_available_ports()
    logger.info(f"All available ports in the system: {all_ports}")
    serial_port = config.get("UART", "UART_PORT")
    if serial_port not in all_ports:
        logger.critical(
            f"Configured serial port {serial_port} is not available in the system. available ports are: {all_ports}")
        raise Exception(
            f"Configured serial port {serial_port} is not available in the system. available ports are: {all_ports}")

    logger.debug(f"Examining provided port {serial_port} against PSoTT protocol")
    if not is_unisat_data_provider(serial_port, timeout=20):
        logger.critical(
            f"Serial port {serial_port} did not send any data that matched the PSoTT protocol")
        raise Exception(
            f"Serial port {serial_port} did not send any data that matched the PSoTT protocol"
        )

    try:
        ser = serial.Serial(port=serial_port, baudrate=9600)
    except serial.SerialException as e:
        logger.critical(e)
        raise Exception("Unable to connect to serial port")
    connected = False
    package = {}

    # local kinto
    local_client = kinto_http.Client(server_url=kinto_local_url,
                                     auth=('admin', kinto_password))
    remote_client = kinto_http.Client(server_url=kinto_remote_url,
                                      auth=('admin', kinto_password))

    thread = threading.Thread(target=read_from_serial, args=(ser,))
    thread.start()

    thread_sync = threading.Thread(target=sync_data, args=(local_client, remote_client, dev_id))
    thread_sync.start()
