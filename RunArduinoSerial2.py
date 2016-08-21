# to figure out which tty port is being used run: dmesg | grep tty

import serial
import time
import RPi.GPIO as GPIO
from Ultrasonic import UltrasonicMeasure



ser = serial.Serial("/dev/ttyUSB0", 9600)

ser.setDTR(True)
time.sleep(1)
ser.setDTR(False)
time.sleep(1)
ser.write('w')

GPIO.setmode(GPIO.BCM)
frontLeft = UltrasonicMeasure(23, 24, 1e-5)
frontLeft.start()

try:
    while True:
    #    input_var = raw_input("Enter a command: ")
    #    ser.write(input_var)
        frontLeftReading = frontLeft.get()
        # ser.write('w')
        print frontLeftReading
        if frontLeftReading < 20 and frontLeftReading >= 0:
            ser.write("h")
            # break
        else:
            ser.write('w')
        time.sleep(0.1)
except KeyboardInterrupt:
    frontLeft.stop()
    GPIO.cleanup()
