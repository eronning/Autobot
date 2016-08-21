# to figure out which tty port is being used run: dmesg | grep tty

import serial
import time
import RPi.GPIO as GPIO
from Ultrasonic import UltrasonicMeasure

SAFETY_THRESHOLD = 12
REFRESHING_INTERVAL = 0.1

ser = serial.Serial("/dev/ttyUSB0", 9600)

def swrite(s):
    ser.write(s)
    print 'SerialW: %s' %s

ser.setDTR(True)
time.sleep(1)
ser.setDTR(False)
# wait for the serial port to be ready before sending the initial command
time.sleep(1)
swrite('w')

GPIO.setmode(GPIO.BCM)
sensors = {}
sensors['frontLeft'] = UltrasonicMeasure(23, 24, 1e-5)
sensors['frontRight'] = UltrasonicMeasure(12, 16, 1e-5)
sensors['left'] = UltrasonicMeasure(17, 27, 1e-5)
sensors['right'] = UltrasonicMeasure(5, 6, 1e-5)
for sensor in sensors.values():
    sensor.start()

try:
    while True:
        time.sleep(REFRESHING_INTERVAL)
        
        valid = True
        readings = {}
        for label, sensor in sensors.items():
            readings[label] = sensor.get()
            if readings[label] < 0:
                valid = False
        if not valid:
            continue
            
        
        print ';'.join(map(lambda x: '%s: %.2f' % (x[0], x[1]), readings.items()))
        
        isObstacleNearby = False
        frontLeftReading = sensors['frontLeft'].get()
        frontRightReading = sensors['frontRight'].get()
        if (frontLeftReading + frontRightReading) / 2 < SAFETY_THRESHOLD:
        # if frontLeftReading < SAFETY_THRESHOLD or frontRightReading < SAFETY_THRESHOLD:
            isObstacleNearby = True
            # if any sensor detects something to close to the car
        if isObstacleNearby:
            swrite('h')
            rightReading = sensors['right'].get()
            leftReading = sensors['left'].get()
            if rightReading > leftReading and rightReading > SAFETY_THRESHOLD:
                swrite('l') # turn to the right 90 degrees
                ser.read(1)
                swrite('I')
                ser.read(1)
                swrite('j')
                ser.read(1)
            elif rightReading <= leftReading and leftReading > SAFETY_THRESHOLD:
                swrite('j') # turn to the left 90 degrees
                ser.read(1)
                swrite('I')
                ser.read(1)
                swrite('l')
                ser.read(1)
            else:
                swrite('k') # turn 180 degrees because both the right and the left are beneath safety threshold
                ser.read(1)
        else:
            if frontLeftReading >= 0 and frontRightReading >= 0:
                swrite('i')
except KeyboardInterrupt:
    swrite('h')
    for sensor in sensors.values():
        sensor.stop()
    GPIO.cleanup()
