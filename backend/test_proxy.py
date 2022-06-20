from RPi import GPIO



class Proximity:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
        
        

    @property
    def status(self):
        return GPIO.inpu(self.pin)


    def on_falling(self, method):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, method, bouncetime=300)
        

proxy = Proximity(26)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN, GPIO.PUD_UP)

def change():
    print("1")
    print(proxy.status)




try:
    proxy.on_falling(change)
    # setup()
    # GPIO.add_event_detect(26, GPIO.BOTH, change, bouncetime=300)
    print("hi")
    while True:
        pass

except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
finally:
    GPIO.cleanup()