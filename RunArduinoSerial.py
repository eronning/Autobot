# to figure out which tty port is being used run: dmesg | grep tty

import serial
import time
import RPi.GPIO as GPIO
from Ultrasonic import UltrasonicMeasure



ser = serial.Serial("/dev/ttyUSB0", 9600)

ser.setDTR(True)
time.sleep(1)
ser.setDTR(False)
ser.write("w")

GPIO.setmode(GPIO.BCM)
#frontLeft = UltrasonicMeasure(23, 24, 1e-5)
#frontLeft.start()

#try:
while True:
	input_var = raw_input("Enter a command: ")
	print input_var
	ser.write(input_var)
		#frontLeftReading = frontLeft.get()
	        #if frontLeftReading < 20 and frontLeftReading >= 0:
		#	ser.write("h")
	        #time.sleep(.01)
#except KeyboardInterrupt:
	#frontLeft.stop()
	#GPIO.cleanup()
ser.write("h")
