from RPi import GPIO
import time

#shiftregister
MR = 13 #active low
SH_CP = 12
ST_CP = 6
OE = 5 #active low
DS = 22


delay = 0.001

class Shiftregister:
    def __init__(self, MR, SHCP, STCP, OE, DS):
        self.MR = MR
        self.SH_CP = SHCP,
        self.ST_CP = STCP
        self.OE = OE
        self.DS = DS

        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.DS,self.OE,self.ST_CP,self.SH_CP,self.MR], GPIO.OUT, initial=GPIO.LOW) #Shiftregister
        GPIO.output(self.MR, GPIO.HIGH)
        self.init_shiftreg()

    def init_shiftreg(self):
        self.reset_shiftreg()
        GPIO.output(self.OE, GPIO.LOW)

    def reset_shiftreg(self):
        GPIO.output(self.MR, GPIO.LOW)
        time.sleep(delay)
        GPIO.output(self.MR, GPIO.HIGH)

    def send_bit(self, bit):
        GPIO.output(self.DS, bit)
        time.sleep(delay)
        GPIO.output(self.SH_CP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(self.DS, GPIO.LOW)
        GPIO.output(self.SH_CP, GPIO.LOW)
        time.sleep(delay)