import time
from datetime import datetime
from RPi import GPIO
#helpers
from helpers.klasseknop import Button
from backend.helpers.ultrasonicClass import Ultrasonic
from helpers.addComment import add_comment
from helpers.buzzerClass import Buzzer
from helpers.LCDClass import ShiftAndLCD
from helpers.sendMeasurements import *
from helpers.mcp3008Class import MCP3008

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
buzz = Buzzer(21)
LCD = ShiftAndLCD(23,24,13,12,6,5,22)
MCP = MCP3008(0,0)

# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


from helpers.socket import Socket
Socket()

@app.route('/')
def hallo():
    print("hallo")
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

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
        Socket.emit_distance(distance)
        send_measurements_to_DB(distance, "ultrasonic")
        voltage = MCP.read(0)
        print(f"{voltage/40.92} V")


        time.sleep(1)

def start_measure_thread():
    print("***starting measurements***")
    measureThread = threading.Thread(target=measuring, args=(), daemon=True)
    measureThread.start()


# ANDERE FUNCTIES


if __name__ == '__main__':
    try:
        #setup LCD
        LCD.write_page0() #IP
        start_chrome_thread()
        start_measure_thread()
        print("**** Starting APP ****")
        socketio.run(app, host='0.0.0.0')
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()

