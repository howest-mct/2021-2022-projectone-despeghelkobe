from repositories.DataRepository import DataRepository
from datetime import datetime
from helpers.relayClass import Relay
from helpers.buzzerClass import Buzzer
import __main__ as main

motorRelay = Relay(17)
buzz = Buzzer(21)


#device ids
ultrasonic_id = 1
voltage_id = 2
gyroscope_id = 3
buzzer_id = 5
valveRelay_id = 6
carmotorRelay_id = 7
hall_id = 9

#tire circumference
tire = 0.07 #m



def sensor_and_actuator_comms(value, sensor):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment = ""
    #code for ultrasonic sensor
    if sensor == "ultrasonic":
        if value < 20:
            comment = "powering off off to avoid crash with wall"
            DataRepository.Add_excecute(carmotorRelay_id, now, "turning the motor off to avoid crashing into a wall")
            motorRelay.circuitbreaker(4)
        DataRepository.Add_measurement(ultrasonic_id, value, now, comment)
        main.emit_ultrasonic(value)

    if sensor == 'volt':
        if value < 4:
            comment = "car batteries low"
        DataRepository.Add_measurement(voltage_id, value, now, comment)
        main.emit_voltage(value)

    if sensor == "gyro":
        if value > 45:
            comment = "car is upside down"
            DataRepository.Add_excecute(buzzer_id, now, "turning buzzer on to notify the car has turned")
            main.emit_upsideDown()
            buzz.send_buzz()

        DataRepository.Add_measurement(gyroscope_id, value, now, comment)

    if sensor == "hall":
        rpm = value * 60
        speed = 0.1885 * rpm * tire #km/h
        DataRepository.Add_measurement(hall_id, speed, now, comment)
        main.emit_speed()
