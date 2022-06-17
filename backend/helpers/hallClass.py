from RPi import GPIO
import datetime

class Hall:
    def __init__(self, pin):
        self.pin = pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.on_change(self.change_detect)
    
    @property
    def magnet_near(self):
        return GPIO.input(self.pin)
    
    def change_detect(self, pin):
        if GPIO.input(self.pin) == GPIO.LOW:
            print('Magnetic material detected')


    def on_change(self, call_method):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, call_method, bouncetime=25)

    