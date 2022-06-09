import time
from datetime import datetime
from RPi import GPIO
#helpers
from helpers.klasseknop import Button
from helpers.ultrasonicClass import Ultrasonic
from helpers.addComment import add_comment
from helpers.buzzerClass import Buzzer
from helpers.LCDClass import ShiftAndLCD
from helpers.sendMeasurements import *
from helpers.mcp3008Class import MCP3008
from helpers.relayClass import Relay

import threading

#flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify


from repositories.DataRepository import DataRepository
from selenium import webdriver

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


ledPin = 21

US_sensor = Ultrasonic(16,20)
LCD = ShiftAndLCD(23,24,13,12,6,5,22)
MCP = MCP3008(0,0)
valveRelay = Relay(19)

#region Code for Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)
CORS(app)

#events
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


# API ENDPOINTS
@app.route('/')
def hallo():
    print("hallo")
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route('/logs')
def logs():
    DataRepository.read_history()

@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on("F2B_boost")
def button():
    # valveRelay.circuitbreaker(1.5)
    print("joost")

#emits
def emit_wallCrash():
    socketio.emit('B2F_wall_crash')

def emit_voltage(value):
    socketio.emit('B2F_send_voltage', {'voltage': value})

def emit_upsideDown():
    socketio.emit('B2F_upside_down')
#endregion




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
        print(f"{distance} cm")
        sensor_and_actuator_comms(distance, "ultrasonic")

        voltage = MCP.read(0)
        print(f"{voltage/40.92} V")
        sensor_and_actuator_comms(voltage, "volt")

        time.sleep(1)
        

def start_measure_thread():
    print("***starting measurements***")
    measureThread = threading.Thread(target=measuring, args=(), daemon=True)
    measureThread.start()
    measureThread.join()


# ANDERE FUNCTIES


if __name__ == '__main__':
    try:
        #setup LCD
        LCD.write_page0() #IP
        valveRelay.on()
        time.sleep(1)
        valveRelay.off()
        start_chrome_thread()
        start_measure_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host="0.0.0.0")
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()

