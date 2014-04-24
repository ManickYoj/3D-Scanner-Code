"""
arduino.py
-------
Author: vascop (GitHub)
Adapted by: Nick Francisci
Status: Complete & Tested
Description: An interface class to wrap the Arduino serial interface

"""

import time
import serial
import sys


class Arduino(object):

    __OUTPUT_PINS = -1

    def __init__(self, port=None, baudrate=115200):
        if not port:
            if sys.platform.startswith('win'):
                port = "COM4"
            elif sys.platform.startswith('lin'):
                port = "/dev/ttyACM0"
            else:
                print("ERROR: unsupported OS!")

        self.serial = serial.Serial(port, baudrate)
        self.serial.write('99')

    def __str__(self):
        return "Arduino is on port %s at %d baudrate" % (self.serial.port,
                                                         self.serial.baudrate)

    def output(self, pinArray):
        self.__sendData(len(pinArray))

        if(isinstance(pinArray, list) or isinstance(pinArray, tuple)):
            self.__OUTPUT_PINS = pinArray
            for each_pin in pinArray:
                self.__sendData(each_pin)
        return True

    def setLow(self, pin):
        self.__sendData('0')
        self.__sendData(pin)
        return True

    def setHigh(self, pin):
        self.__sendData('1')
        self.__sendData(pin)
        return True

    def getState(self, pin):
        self.__sendData('2')
        self.__sendData(pin)
        return self.__formatPinState(self.__getData()[0])

    def analogWrite(self, pin, value):
        self.__sendData('3')
        self.__sendData(pin)
        self.__sendData(value)
        return True

    def analogRead(self, pin):
        self.__sendData('4')
        self.__sendData(pin)
        return self.__getData()

    def turnOff(self):
        for each_pin in self.__OUTPUT_PINS:
            self.setLow(each_pin)
        return True

    def __sendData(self, serial_data):
        while(self.__getData()[0] != "w"):
            pass
        self.serial.write(str(serial_data))

    def __getData(self):
        return self.serial.readline().rstrip('\n')

    def __formatPinState(self, pinValue):
        if pinValue == '1':
            return True
        else:
            return False

    def __exit__(self, type, value, tb):
        self.turnOff()
        self.close()

    def close(self):
        self.serial.close()
        return True


if __name__ == '__main__':
    a = Arduino()
    a.output([5])
    time.sleep(0.1)
    a.setHigh(5)
    time.sleep(5)
    a.setLow(5)
