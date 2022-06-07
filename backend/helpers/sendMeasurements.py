from repositories.DataRepository import DataRepository
from datetime import datetime


def send_measurements_to_DB(value, sensor):

    #code for ultrasonic sensor
    if sensor == "ultrasonic":
        comment = ""
        if value < 20:
            comment = "powering off off to avoid crash with wall"
            
        DataRepository.Add_measurement(1, value, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), comment)