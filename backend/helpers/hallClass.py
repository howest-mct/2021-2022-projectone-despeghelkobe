from RPi import GPIO
import time

class Hall:
    def __init__(self, pin):
        self.pin = pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.on_change(self.change_detect)
        
    
    __counter = 0
    __start_time = time.time()

    @property
    def rps(self):
        stop_time = time.time()
        delta_time = stop_time - self.__start_time
        rps = self.__counter/ delta_time
        
        self.__counter = 0
        self.__start_time = time.time()
        return rps
    
    def change_detect(self, pin):
        self.__counter+=1
        


    def on_change(self, call_method):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, call_method, bouncetime=50)
        

    