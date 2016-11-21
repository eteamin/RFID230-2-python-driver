import binascii
import struct

import serial
from serial.serialutil import SerialException

from rfid.exceptions import *


def as_bytes(number):
    output = []
    while number:
        output.insert(0, number % 256)
        number >>= 8
    return output


STX = 0x02
RESPONSE_FORMAT = 'bbb'


class Driver(object):
    def __init__(self, serial_path, timeout, encrypion_key):
        self.serial_path = serial_path
        self.timeout = timeout
        self.encryption_key = encrypion_key
        self.status = None

    def communicate(self, command, data=[]):
        address = 0x0
        length = 1 + len(data)
        bcc = address ^ length ^ command
        for b in data:
            bcc ^= b
        if len(data):
            i = struct.pack('BBBB%sBB' % len(data), STX, address, length, command, *(data + [bcc]))
        else:
            i = struct.pack('BBBBB', STX, address, length, command, bcc)
        ser = serial.Serial(self.serial_path, 9600, timeout=self.timeout)

        ser.write(i)
        header = ser.read(3)
        stx, address, resp_len, = struct.unpack(RESPONSE_FORMAT, header)
        self.status = struct.unpack('b', ser.read(1))[0]
        self.interpret_status()
        data = ser.read(resp_len - 1)
        return binascii.b2a_hex(data)

    def interpret_status(self):
        if self.status == 0:
            pass
        elif self.status == 1:
            raise NoCardError
        elif self.status == 2:
            raise AntiColError
        elif self.status == 3:
            raise BitCounterError
        elif self.status == 4:
            raise ReturnDataError
        elif self.status == 5:
            raise AuthError
        elif self.status == 10:
            raise ProgrammingError
        elif self.status == 11:
            raise UnknownError
        elif self.status == 13:
            raise OperationError
