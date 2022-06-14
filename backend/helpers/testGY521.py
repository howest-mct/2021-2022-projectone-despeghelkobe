import smbus
import math
 
# Register
PWR_MGMT_1   = 0x6B
PWR_MGMT_2 = 0x6c
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) for Revision 1
address = 0x68       # via i2cdetect
 
# Activate to be able to address the module
bus.write_byte_data(address, PWR_MGMT_1, 0)
 
print("gyro")
print("--------")
 
gyro_xout = read_word_2c(0x43)
gyro_yout = read_word_2c(0x45)
gyro_zout = read_word_2c(0x47)
 
print ("gyro_xout: ", ("%5d" % gyro_xout), " skaliert: ", (gyro_xout / 131))
print ("gyro_yout: ", ("%5d" % gyro_yout), " skaliert: ", (gyro_yout / 131))
print ("gyro_zout: ", ("%5d" % gyro_zout), " skaliert: ", (gyro_zout / 131))

print("accelero")
print("---------------------")
 
accelero_xout = read_word_2c(0x3b)
accelero_yout = read_word_2c(0x3d)
accelero_zout = read_word_2c(0x3f)
 
accelero_xout_scaled = accelero_xout / 16384.0
accelero_yout_scaled = accelero_yout / 16384.0
accelero_zout_scaled = accelero_zout / 16384.0
 
print("accelero_xout: ", ("%6d" % accelero_xout), " scaled: ", accelero_xout_scaled) 
print("accelero_yout: ", ("%6d" % accelero_yout), " scaled: ", accelero_yout_scaled) 
print("accelero_zout: ", ("%6d" % accelero_zout), " scaled: ", accelero_zout_scaled) 
 
print("X Rotation: " , get_x_rotation(accelero_xout_scaled, accelero_yout_scaled, accelero_zout_scaled))
print("Y Rotation: " , get_y_rotation(accelero_xout_scaled, accelero_yout_scaled, accelero_zout_scaled))