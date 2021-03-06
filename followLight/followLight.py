
# to figure out which tty port is being used run: dmesg | grep tty

import serial
import time
import RPi.GPIO as GPIO
from Ultrasonic import UltrasonicMeasure
import logging
# logging.getLogger.setLevel(logging.DEBUG)
# import findBeacon # return maximu value of lumi
# import existObstacle # return bool value if obstacle is in front
# import avoidObstacle # need to modify these function, if no obstacle around, should stop instead of moving fowrad

#while
 #step1 findBeacon(), if return value<threshhold_ambient go to step 3
 #step2 ifObstacle(), if yes go to step 3, if no go to step 4
 #step3 move forward one step, go back to step 1
 #step4 avoidObstacle(), go back to step 1
#rest at the beacon

threshhold_final = 80     # reacod the max lum at 0 distance
threshhold_ambient = 4    # record ambient value

max_lum = 0
time_fullturn = 6 # doesnot to be accurate, as long as find the maixmum value

SAFETY_THRESHOLD = 20
REFRESHING_INTERVAL = 0.1
ultrasonicsensors = {}
GPIO.setmode(GPIO.BCM)

ser_light = serial.Serial("/dev/ttyACM0", 9600)
ser_motor = serial.Serial("/dev/ttyUSB0",9600)

# Initialize the Serial Ports for Light Sensor and Motor Driver
print "Insert the key..."
ser_light.setDTR(True)
time.sleep(1)
print "Rotate the key..."
ser_light.setDTR(False)
time.sleep(1)
print "Igniting the enginee..."
ser_motor.setDTR(True)
time.sleep(1)
print "Try again..."
ser_motor.setDTR(False)

def swrite(ser, s):
    ser.write(s)
    logging.getLogger('swrite').debug(s)
def sreadline(ser):
    read_str = ser.readline()
    logging.getLogger('sreadline').debug(read_str)
    return read_str
def sread(ser, count=None):
    read_str = ser.read(count)
    logging.getLogger('sread').debug(read_str)
    return read_str
    
def readLightSensor():
    reading = None
    while True:
        swrite(ser_light, 'a')
        reading_str = sreadline(ser_light).strip()
        if len(reading_str) > 0:
            try:
                reading = int(reading_str)
                logging.getLogger('readLightSensor').info(str(reading))
            except ValueError:
                continue
            break
    return reading

def findBeacon():
    swrite(ser_motor, 'o')
    max_lum = -1
    start = time.time()
    while(time.time()-start<time_fullturn):
        reading = readLightSensor()
        print 'reading@findBeacon: %d' % reading
        if(max_lum < reading):
            max_lum = reading # get the max luminence value after one full turn
    print 'max_lum@findBeacon: %d' % max_lum
    return max_lum  # return the max lumi

def startUltrasonic():
    global ultrasonicsensors
    # Initialize Ultrasonic Senors
    ultrasonicsensors['frontLeft'] = UltrasonicMeasure(23, 24, 1e-5)
    ultrasonicsensors['frontRight'] = UltrasonicMeasure(12, 16, 1e-5)
    ultrasonicsensors['left'] = UltrasonicMeasure(17, 27, 1e-5)
    ultrasonicsensors['right'] = UltrasonicMeasure(5, 6, 1e-5)
    for sensor in ultrasonicsensors.values():
        sensor.start()
        
def endUltrasonic():
    global ultrasonicsensors
    for sensor in ultrasonicsensors.values():
        sensor.stop()
    
def existObstacle():
    global ultrasonicsensors
    isObstacleNearby = None
    try:
        while True:
            time.sleep(REFRESHING_INTERVAL)
            
            valid = True
            readings = {}
            for label, sensor in ultrasonicsensors.items():
                readings[label] = sensor.get()
                if readings[label] < 0:
                    valid = False
            logging.getLogger('existObstacle').info(
                ';'.join(map(lambda x: '%s: %.2f' % (x[0], x[1]), readings.items())))
            if not valid:
                continue
            
            
            isObstacleNearby = False
            frontLeftReading = ultrasonicsensors['frontLeft'].get()
            frontRightReading = ultrasonicsensors['frontRight'].get()
            if (frontLeftReading + frontRightReading) / 2 < SAFETY_THRESHOLD:
            # if frontLeftReading < SAFETY_THRESHOLD or frontRightReading < SAFETY_THRESHOLD:
                isObstacleNearby = True
                # if any sensor detects something to close to the car
            break
    except KeyboardInterrupt:
        raise
    return isObstacleNearby

if __name__ == '__main__':
    startUltrasonic()
    # print findBeacon()
    # # print existObstacle()
    # endUltrasonic()

    try:
        flag = 1;
        while(readLightSensor() < threshhold_final):
            print 'state: %d' % flag
            if(flag == 1):
                # find direction
                L_read = findBeacon()
                print 'L_read: %d' % L_read
		if(L_read >= threshhold_final):
		    break
                if(L_read < threshhold_ambient):
                    flag = 2
                else:
                    flag = 2
                    swrite(ser_motor, "a")
                    deadline = time.time() + 10
                    while(readLightSensor() < L_read * .9 and time.time() < deadline): # -20 tolerabce
                        time.sleep(0.01)
                    swrite(ser_motor, "h")
                    L_read = 0
            elif(flag == 2):
                # check obstacle
                if(existObstacle()):
                    flag = 4
                else:
                    flag = 3
            elif(flag == 3):
                # move forward to find the beacon
                swrite(ser_motor, "I")
                sread(ser_motor, 1)
                flag = 1
            elif(flag == 4):
                # get around the obstacle
		print "turning right 90 degrees"
		swrite(ser_motor, "l")
		sread(ser_motor, 1)
		print "going forward for a short cycle"
		swrite(ser_motor, "I")
		sread(ser_motor, 1)
		print "halting car"
		swrite(ser_motor, "h")
		print "turning left 90 degrees"
		swrite(ser_motor, "j")
		sread(ser_motor, 1)
                flag = 1
    finally:
        swrite(ser_motor, "h")
        endUltrasonic()
