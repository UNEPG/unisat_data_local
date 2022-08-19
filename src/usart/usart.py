import serial

from serial.tools.list_ports_common import ListPortInfo


def list_all_available_ports():
    """List all ports and get device as list"""
    from serial.tools import list_ports
    list_port_info: ListPortInfo = list_ports.comports()
    result = [each.device for each in list_port_info]
    return result


def is_unisat_data_provider(port: str, timeout: int = 10) -> bool:
    """Check if the port is correct for UniSat Data Provider.
    We check this by reading 10 seconds of serial data and compare the received bytes with the PSoTT
    protocol.
    """
    with serial.Serial(port=port, baudrate=9600, timeout=timeout) as ser:
        s = ser.read(100)  # read 10 byte
        decoded = s.decode('utf-8')
    return 'subID' in decoded
