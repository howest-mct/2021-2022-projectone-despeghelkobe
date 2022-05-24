from RPi import GPIO
import time

class Ultrasonic:
    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo
        self.start = 0
        self.stop = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

    @property
    def distance(self):
        self.stop = time.time()
        timedif = self.stop - self.start
        afstand = (timedif * 34300)/2
        return afstand

    def measure(self):
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
        while GPIO.input(self.echo)==0:
            self.start = time.time()
        while GPIO.input(self.echo)==1:
            self.stop = time.time()

    # def on_echo_receive(self, call_method):
    #     GPIO.add_event_detect(self.echo, GPIO.FALLING, call_method, bouncetime=500)
        