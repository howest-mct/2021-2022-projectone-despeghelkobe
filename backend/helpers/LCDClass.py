from RPi import GPIO
import time
from subprocess import check_output

class ShiftAndLCD:
    __delay = 0.001
    __page = 0
    def __init__(self, RS, E, MR, SHCP, STCP, OE, DS):
        #LCD
        self.RS = RS
        self.E = E

        #SHIFT
        self.MR = MR
        self.SH_CP = SHCP
        self.ST_CP = STCP
        self.OE = OE
        self.DS = DS

        GPIO.setmode(GPIO.BCM)
        GPIO.setup([RS,E], GPIO.OUT)
        GPIO.setup([self.DS,self.OE,self.ST_CP,self.SH_CP,self.MR], GPIO.OUT, initial=GPIO.LOW) #Shiftregister
        GPIO.output(self.MR, GPIO.HIGH)


        self.init_shiftreg()
        self.init_LCD()

    


    def init_shiftreg(self):
            self.reset_shiftreg()
            GPIO.output(self.OE, GPIO.LOW)

    
    def init_LCD(self):
        function_set = 0x38 # 0b00111000
        display_on = 0x0C   # 0b00001100
        CD_and_CH = 0x01    # 0b00000001
        self.send_instruction(function_set)
        self.send_instruction(display_on)
        self.send_instruction(CD_and_CH)

    def reset_shiftreg(self):
        GPIO.output(self.MR, GPIO.LOW)
        time.sleep(self.__delay)
        GPIO.output(self.MR, GPIO.HIGH)

    def send_bit_LCD(self, bit):
        GPIO.output(self.DS, bit)
        time.sleep(self.__delay)
        GPIO.output(self.SH_CP, GPIO.HIGH)
        time.sleep(self.__delay)
        GPIO.output(self.DS, GPIO.LOW)
        GPIO.output(self.SH_CP, GPIO.LOW)
        time.sleep(self.__delay)

    def send_byte_LCD(self, byte):
        GPIO.output(self.E,GPIO.HIGH)
        mask = 0x80 # 0b10000000
        for x in range(0,8):
            bit = ((byte << x) & mask)
            self.send_bit_LCD(bit)
        self.copy_to_storage_register()
        GPIO.output(self.E,GPIO.LOW)

    def copy_to_storage_register(self):
        GPIO.output(self.ST_CP, GPIO.HIGH)
        time.sleep(self.__delay)
        GPIO.output(self.ST_CP, GPIO.LOW)
        time.sleep(self.__delay)

    def send_char(self, char):
        GPIO.output(self.RS, GPIO.HIGH)
        self.send_byte_LCD(char)
        time.sleep(self.__delay)
    
    def send_instruction(self, instruction):
        GPIO.output(self.RS, GPIO.LOW)
        self.send_byte_LCD(instruction)
        time.sleep(self.__delay)

    def write_text(self, text):
        for char in text:
            self.send_char(ord(char))

    def set_cursor(self, row, position, page):
        hexrow1 = 0x00 | (page) << 4
        hexrow2 = 0x40 | (page) << 4
        coords = 0
        if row == 0:
            coords = hexrow1 | (position)
        else:
            coords = hexrow2 | (position)
        self.send_instruction(coords | 0x80)

    def write_page0(self): #IP
        ip = str(check_output(['hostname','--all-ip-addresses']))
        ip = ip[18:33]
        self.set_cursor(0,0,0)
        self.write_text(ip)
