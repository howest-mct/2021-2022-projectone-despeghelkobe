from RPi import GPIO
import time
from subprocess import check_output
import threading


#shiftregister
MR = 13 #active low
SH_CP = 12
ST_CP = 6
OE = 5 #active low
DS = 22

#LCD
RS = 23
E = 24


delay = 0.001
page = 0

def setup_LCD_and_shift():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([RS,E], GPIO.OUT) #LCD
    GPIO.setup([DS,OE,ST_CP,SH_CP,MR], GPIO.OUT, initial=GPIO.LOW) #Shiftregister
    GPIO.output(MR, GPIO.HIGH) #set MR high
    


# LCD & shiftregister
def init_shiftreg():
    reset_shiftreg()
    GPIO.output(OE, GPIO.LOW)

def init_LCD():
    function_set = 0x38 # 0b00111000
    display_on = 0x0C   # 0b00001100
    CD_and_CH = 0x01    # 0b00000001
    send_instruction(function_set)
    send_instruction(display_on)
    send_instruction(CD_and_CH)


def reset_shiftreg():
    GPIO.output(MR, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(MR, GPIO.HIGH)


def send_bit_LCD(bit):
    GPIO.output(DS, bit)
    time.sleep(delay)
    GPIO.output(SH_CP, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(DS, GPIO.LOW)
    GPIO.output(SH_CP, GPIO.LOW)
    time.sleep(delay)


def send_byte_LCD(byte):
    GPIO.output(E,GPIO.HIGH)
    mask = 0x80 # 0b10000000
    for x in range(0,8):
        bit = ((byte << x) & mask) #normaal met "> 0" erna maar in python hoeft dit niet bij bitoperaties
        send_bit_LCD(bit)
    copy_to_storage_register()
    GPIO.output(E,GPIO.LOW)
    #reset_shiftreg()

def copy_to_storage_register():
    GPIO.output(ST_CP, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(ST_CP, GPIO.LOW)
    time.sleep(delay)
    #print("storage clock aan en uit zetten")

def send_char(char):
    GPIO.output(RS, GPIO.HIGH)
    send_byte_LCD(char)
    time.sleep(delay)

def send_instruction(instruction):
    GPIO.output(RS, GPIO.LOW)
    send_byte_LCD(instruction)
    time.sleep(delay)

def next_page_LCD():
    global page
    print("pushed")
    print(page)
    instruction = 0x18 # 0b00011000 (goes 1 cell to the right)
    if page == 2: #goto page 0
        send_instruction(2) #0b00000010 (back to page 1)
        write_page0()
        page = 0
    else:
        if page == 0: #goto page 1
            for x in range(0,16):
                send_instruction(instruction)
            set_cursor(1,2,1)
            write_text("X")
        else: #page == 1 #goto page 2
            set_cursor(1,2,1)
            write_text("Y")
        page += 1

def write_text(text):
    for char in text:
        send_char(ord(char))

def set_cursor(row, position, page):
    hexrow1 = 0x00 | (page) << 4
    hexrow2 = 0x40 | (page) << 4
    coords = 0
    if row == 0:
        coords = hexrow1 | (position)
    else:
        coords = hexrow2 | (position)
    send_instruction(coords | 0x80)

def write_page0(): #IP
    ip = str(check_output(['hostname','--all-ip-addresses']))
    ip = ip[18:33]
    print(ip)
    set_cursor(0,0,0)
    write_text(ip)