import RPi.GPIO as GPIO
import time
import logging
import sys
from threading import Thread, Lock, RLock

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler(sys.stderr))

DISCOUNT = .4

class UltrasonicMeasure:
    trigger_width = 1e-5
    echo_unit = 1e-5
    def __init__(self, trigger_port, echo_port, time_interval):
        # GPIO.setmode(GPIO.BCM)
        self.running = False
        self.runningLock = RLock()
        self.measurement = -1
        self.measurementLock = RLock()
        self.time_interval = time_interval
    
        self.trigger_port = trigger_port
        self.echo_port = echo_port
        GPIO.setup(trigger_port, GPIO.OUT)
        GPIO.setup(echo_port, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        self.t = Thread(name='measurement_service', target=self.auto_measure)
        
    def auto_measure(self):
        while True:
            self.runningLock.acquire()
            try:
                if not self.running:
                    break
            finally:
                self.runningLock.release()
            logger.debug('start a measurement by auto_measure')
            try:
                measurement = self.measure()
            except:
                logger.warning("exception when measuring", exc_info=sys.exc_info())
                raise
            self.measurementLock.acquire()
            try:
                if measurement > 0:
                    if self.measurement < 0:
                        self.measurement = measurement
                    else:
                        self.measurement = DISCOUNT * self.measurement + (1 - DISCOUNT) * measurement
            finally:
                self.measurementLock.release()
            time.sleep(self.time_interval)
        
    def measure(self):
        GPIO.output(self.trigger_port, GPIO.LOW)
        time.sleep(UltrasonicMeasure.trigger_width)
        GPIO.output(self.trigger_port, GPIO.HIGH)
        time.sleep(UltrasonicMeasure.trigger_width)
        GPIO.output(self.trigger_port, GPIO.LOW)
        echoed = False
        count = 0
        waiting_count = 0
        # TODO: add filtering to avoid noise
        while waiting_count < 5000:
            time.sleep(UltrasonicMeasure.echo_unit)
            r = GPIO.input(self.echo_port)
            if r:
                echoed = True
                count += 1
            elif echoed:
                break
            waiting_count += 1
        logger.debug('measure: %d' % count)
        return count
        
    def start(self):
        self.running = True
        self.t.start()
        
    def stop(self):
        self.runningLock.acquire()
        try:
            self.running = False
        finally:
            self.runningLock.release()
    
    def get(self):
        self.measurementLock.acquire()
        try:
            val = self.measurement
        finally:
            self.measurementLock.release()
        return val

if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    s = UltrasonicMeasure(23, 24, 1e-5)
    s.start()
    try:
        while True:
            print s.get()
            time.sleep(1)
    except KeyboardInterrupt:
        s.stop()
        GPIO.cleanup()
