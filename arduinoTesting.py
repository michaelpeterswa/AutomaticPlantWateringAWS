#tests the serial communications for arduino

import serial
import io
import time

ser = serial.Serial('/dev/ttyACM0')
print(ser.name)
ser.baudrate = 9600
ser.timeout = 1
print("Port open: " + str(ser.is_open))

sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

while True:
    ser.reset_input_buffer()
    if (ser.is_open):
        sio.write("0\n")
        sio.flush()
        print("wrote 0")
        while ser.inWaiting() == 0:
            print("Waiting for data")
            time.sleep(.5)
        print("bytes: " + str(ser.inWaiting()))
        dataIn = sio.read()
        print(dataIn)
        print("data read")
    else:
        print("port not open")
