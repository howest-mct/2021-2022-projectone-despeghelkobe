from RPi import GPIO
import time

class Relay():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
    
    def on(self):
        GPIO.output(self.pin, True)
    
    def off(self):
        GPIO.output(self.pin, False)

    def circuitbreaker(self,sec):
        GPIO.output(self.pin, True)
        time.sleep(sec)
        GPIO.output(self.pin, False)

