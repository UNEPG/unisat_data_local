import serial

from serial.tools.list_ports_common import ListPortInfo

from src.helpers.objects import get_cls_attrs


def c2_1_1():
    """Open port with no timeout"""
    ser = serial.Serial(port="/dev/cu.usbmodem83201", baudrate=9600, timeout=1)  # open serial port
    print(ser.name)  # check which port was really used
    # bytes = b'...' literals = a sequence of octets (integers between 0 and 255)
    """
    >>> print(out)
    b'hello,Python!'
    >>> out.decode('utf-8')
    'hello,Python!'
    """
    ser.write(b"hello")
    ser.close()


def c2_1_2():
    """Open named port at "9600,8,N,1" """
    with serial.Serial(port="/dev/cu.usbmodem83201", baudrate=9600, timeout=1) as ser:
        x = ser.read()  # read one byte
        s = ser.read(10)  # read 10 byte
        line = ser.readline()  # read a `\n` terminated line


def c2_1_3():
    """Open port at 9600,8,E,1 non blocking HW handshaking """
    ser = serial.Serial(port="/dev/cu.usbmodem83201", baudrate=9600, timeout=0, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE)


def c2_2():
    """Get a Serial instance and configure/open it later"""
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = "/dev/cu.usbmodem83201"
    print(ser)
    print(ser.open())
    print(ser.is_open)
    print(ser.close())


def c2_3():
    with serial.Serial() as ser:
        ser.baudrate = 9600
        ser.port = "/dev/cu.usbmodem83201"
        print(ser)
        print(ser.open())
        print(ser.is_open)
        print(ser.write(b"hello"))


def c2_3_1():
    import io
    ser = serial.serial_for_url('loop://', timeout=1)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

    sio.write("hello\n")
    sio.flush()  # It is buffering. required to get the data out
    hello = sio.readline()
    print(hello == "hello\n")


def c2_4():
    """List all ports"""
    from serial.tools import list_ports
    list_port_info: ListPortInfo = list_ports.comports()
    for each in list_port_info:
        print("-------------------Serial Device Info-------------------")
        all_attrs = get_cls_attrs(each)
        for key in all_attrs:
            print(f"{key} = {getattr(each, key)}")


def c2_4_1():
    """List all ports and get device as list"""
    from serial.tools import list_ports
    list_port_info: ListPortInfo = list_ports.comports()
    result = [each.device for each in list_port_info]
    return result


def is_unisat_data_provider(port: str) -> bool:
    """Check if the port is correct for UniSat Data Provider.
    We check this by reading 10 seconds of serial data and compare the received bytes with the PSoTT
    protocol.
    """
    with serial.Serial(port=port, baudrate=9600, timeout=10) as ser:
        s = ser.read(100)  # read 10 byte
        decoded = s.decode('utf-8')
    return 'subID' in decoded


# run the selected one
# c2_1_1()
# c2_1_2()
# c2_1_3()
# c2_2()
# c2_3()
# c2_3_1()
# c2_4()
# print(c2_4_1())

all_ports = c2_4_1()
is_unisat_data_provider(all_ports[0])
