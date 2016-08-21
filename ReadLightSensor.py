# to figure out which tty port is being used run: dmesg | grep tty

import serial
import time

ser = serial.Serial("/dev/ttyACM0", 115200)

ser.setDTR(True)
time.sleep(1)
ser.setDTR(False)


while True:
	lightVal = ser.readline()
	print lightVal
	
