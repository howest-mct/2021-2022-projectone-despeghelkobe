import smbus			#import SMBus module of I2C
import time         #import

 
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

#global variables
bus = smbus.SMBus(1)
Device_Address = 0x68
gyro_scale_factor = 16384.0
accelero_scale_factor = 131.0
sleep = 0.1


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)
    
    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value

def read_accelero():
    #read accelero raw
    accelero = []
    accelero.append(read_raw_data(ACCEL_XOUT_H))
    accelero.append(read_raw_data(ACCEL_YOUT_H))
    accelero.append(read_raw_data(ACCEL_ZOUT_H))
    return accelero


def read_gyro():
    #Read Gyro raw
    gyro_x = read_raw_data(GYRO_XOUT_H)/gyro_scale_factor
    gyro_y = read_raw_data(GYRO_YOUT_H)/gyro_scale_factor
    gyro_z = read_raw_data(GYRO_ZOUT_H)/gyro_scale_factor
    return gyro_x, gyro_y, gyro_z

def refactor_data(valueList, scale_factor):
    newValueList = []
    for value in valueList:
        newValueList.append(value/scale_factor)
    return newValueList

def calc_velocity(accel):
    print(f"acceleration: {accel} g")
    accel = accel*(9.8066*sleep)
    final_vel = accel*sleep
    print(f"velocity: {final_vel} m/s")

def calc_angle(angularSpeed):
    current_angle = prev_angle + angularSpeed*sleep
    #print(current_angle)



try:
    MPU_Init()
    prev_angle = 0
    while True:
        #Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)
        
        #Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)
        
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0
        
        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0

        calc_velocity(Az)

        calc_angle(Gx)

        #print(f"Gx={Gx} °/s \tGy={Gy} °/s \tGz={Gz} °/s \nAx={Ax} g \tAy={Ay} g \tAz={Az} g")
        time.sleep(sleep)

except KeyboardInterrupt:
    print("exception caught")
finally:
    pass