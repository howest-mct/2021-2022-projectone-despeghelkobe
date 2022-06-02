import time
from datetime import datetime
from RPi import GPIO
from helpers.klasseknop import Button
from helpers.ultrasonic import Ultrasonic
from helpers.addComment import add_comment
from helpers.buzzerClass import Buzzer
from helpers.LCDClass import ShiftAndLCD
import threading


from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository

from selenium import webdriver

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


ledPin = 21

US_sensor = Ultrasonic(16,20)
buzz = Buzzer(21)
LCD = ShiftAndLCD(23,24,13,12,6,5,22)


# Code voor Hardware
def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    

# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


from helpers.socket import Socket
Socket()

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)
# API ENDPOINTS
@socketio.on('connect')
def initial_connection():
    print('A new client connect')

import socket

@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

# @socketio.on("F2B_btn_click")
# def button():
#     print("test")



# @socketio.on('F2B_switch_light')
# def switch_light(data):
#     # Ophalen van de data
#     lamp_id = data['lamp_id']
#     new_status = data['new_status']
#     print(f"Lamp {lamp_id} wordt geswitcht naar {new_status}")

#     # Stel de status in op de DB
#     res = DataRepository.update_status_lamp(lamp_id, new_status)

#     # Vraag de (nieuwe) status op van de lamp en stuur deze naar de frontend.
#     data = DataRepository.read_status_lamp_by_id(lamp_id)
#     socketio.emit('B2F_verandering_lamp', {'lamp': data}, broadcast=True)

#     # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
#     if lamp_id == '3':
#         print(f"TV kamer moet switchen naar {new_status} !")
#         GPIO.output(ledPin, new_status)


def main():
    while True:
        time.sleep(0.0001)

def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=main, args=(), daemon=True)
    thread.start()


def start_chrome_kiosk():
    import os

    os.environ['DISPLAY'] = ':0.0'
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--kiosk')
    # chrome_options.add_argument('--no-sandbox')         
    # options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost")
    while True:
        time.sleep(0.0001)


def start_chrome_thread():
    print("**** Starting CHROME ****")
    chromeThread = threading.Thread(target=start_chrome_kiosk, args=(), daemon=True)
    chromeThread.start()

def measuring():
    while True:
        # ultrasonic sensor
        distance = US_sensor.measure()
        print(distance)
        socketio.emit('B2F_send_distance', {'distance': distance})
        DataRepository.Add_measurement(1, distance, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), add_comment(1, distance))
        

        time.sleep(1)



def start_measure_thread():
    print("***starting measurements***")
    measureThread = threading.Thread(target=measuring, args=(), daemon=True)
    measureThread.start()


# ANDERE FUNCTIES


if __name__ == '__main__':
    try:
        setup_gpio()

        #setup LCD
        LCD.write_page0() #IP

        # start_thread()
        start_chrome_thread()
        start_measure_thread()
        print("**** Starting APP ****")
        socketio.run(app, host='0.0.0.0')
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()

