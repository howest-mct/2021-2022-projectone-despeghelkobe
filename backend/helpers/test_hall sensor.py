from RPi import GPIO
import time

#Hall sensor is connected to pin 11 (BOARD-Layout!)
HALL = 27


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(HALL,GPIO.IN, pull_up_down=GPIO.PUD_UP)

def change_detected(pin):
    if GPIO.input(HALL) == GPIO.LOW:
        pass
    else:
        pass


# Register event-listener on falling and raising
# edge on HALL-sensor input. Call "change_detected" as
# callback
def on_change():
    GPIO.add_event_detect(HALL, GPIO.RISING, change_detected, bouncetime=25)


hall_tresh = 10
# The main-loop does nothing. All is done by the event-listener
try:
    setup()
    # on_change()

    
    while True:
        on_state = False
        hall_count = 1
        start_time = time.time()
        while hall_count <= hall_tresh:
            if(GPIO.input(HALL) == GPIO.LOW):
                if(on_state == False):
                    on_state = True
                    hall_count+=1
                    print("yeet")
            if(GPIO.input(HALL) == GPIO.HIGH):
                if(on_state == True):
                    on_state = False
        time.sleep(0.01)
        
        end_time = time.time()
        delta_time = end_time-start_time
        rpm = hall_count/delta_time
        print(rpm)
        time.sleep(0.1)



# Quit on Ctrl-c
except KeyboardInterrupt:
    print('KeyboardInterrupt exception is caught')

# Cleanup GPIO
finally:
    GPIO.cleanup() 
