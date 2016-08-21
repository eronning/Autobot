import RPi.GPIO as GPIO
import time

triggerPin = 23
echoPin = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
	while True:
		GPIO.output(triggerPin, GPIO.LOW)
		time.sleep(1)
		GPIO.output(triggerPin, GPIO.HIGH)
		time.sleep(1e-5)
		GPIO.output(triggerPin, GPIO.LOW)
		echoed = False
		count = 0
		waiting_count = 0
		while waiting_count < 100000:
			time.sleep(1e-5)
			r = GPIO.input(echoPin)
			if r:
				echoed = True
				count += 1
			elif echoed:
				break
			waiting_count += 1

		print echoed
		print count
except KeyboardInterrupt:
	GPIO.cleanup()
