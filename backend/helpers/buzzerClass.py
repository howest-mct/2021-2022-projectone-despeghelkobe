from RPi import GPIO
import time

class Buzzer:
    def __init__(self, pin):
        self.pin = pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def send_buzz(self):
        GPIO.output(self.pin, True)
        time.sleep(1)
        GPIO.output(self.pin, False)
