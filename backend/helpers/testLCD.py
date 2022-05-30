from RPi import GPIO
import time


#shiftregister
MR = 13 #active low
SH_CP = 12
ST_CP = 6
OE = 5 #active low
DS = 22

#LCD
RS = 23
E = 24


A = 1 << 0#A = P0
B = 1 << 1#B = P1
C = 1 << 2#C = P2
D = 1 << 3#D = P3
E = 1 << 4#E = P4
F = 1 << 5#F = P5
G = 1 << 6#G = P6
H = 1 << 7#H = P7



delay = 0.001
statusDisplay = True

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([MR, SH_CP, ST_CP, OE, DS], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup([RS,E], GPIO.OUT, initial=GPIO.OUT)


def init_shift_register():
    GPIO.output(MR, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(MR, GPIO.HIGH)
    #print("reset shift register")
    GPIO.output(OE, GPIO.LOW)
    #print("output enable aanzetten")

def init_LCD():
    function_set = 0x38 # 0b00111000
    display_on = 0x0F   # 0b00001111
    CD_and_CH = 0x01    # 0b00000001
    send_instruction(function_set)
    send_instruction(display_on)
    send_instruction(CD_and_CH)

def send_character(value):
    GPIO.output(RS, GPIO.HIGH)
    write_one_byte(value)
    time.sleep(delay)

def send_instruction(value):
    GPIO.output(RS, GPIO.LOW)
    write_one_byte(value)
    time.sleep(delay)

def write_message(text):
    if len(text)>16:
        #langer dan 16
        text1 = text[:16]
        text2 = text[16:]
        for char in text1:
            send_character(ord(char))
        
        set_cursor(2,1)

        for char in text2:   
            send_character(ord(char))
    else:
        #korter of even lang als 16
        for char in text:
            send_character(ord(char))

def set_cursor(row,position):
    if row == 1:
        position = 0x00 | (position-1)
    else:
        position = 0x40 | (position-1)
    send_instruction(position | 0x80)


#shiftregister
def write_one_byte(byte):
    #print(bin(byte))
    GPIO.output(E, GPIO.HIGH)
    mask = 0x80 # 0b10000000
    for x in range(0,8):
        bit = (byte & mask >> x) #normaal met "> 0" erna maar in python hoeft dit niet bij bitoperaties
        write_one_bit(bit)
    GPIO.output(E, GPIO.LOW)

def write_one_bit(bit):
    GPIO.output(DS, bit)
    time.sleep(delay)
    GPIO.output(SH_CP, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(DS, GPIO.LOW)
    GPIO.output(SH_CP, GPIO.LOW)
    time.sleep(delay)

def copy_to_storage_register():
    GPIO.output(ST_CP, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(ST_CP, GPIO.LOW)
    time.sleep(delay)
    #print("storage clock aan en uit zetten")

   

try:
    setup()
    init_shift_register()
    while 1:
        if statusDisplay == True:
            for x in range(0,7):
                write_message("hey")
                copy_to_storage_register()
                time.sleep(1)
        


except KeyboardInterrupt as e:
    print(e)
finally:
    GPIO.cleanup()







