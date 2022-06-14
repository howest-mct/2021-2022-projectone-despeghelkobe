def add_comment(device_id,value):

    if(device_id == 1):
        if(value < 20):
                return "power off to avoid crash with wall"
    if(device_id == 2):
        if(value < 4.05):
            return "batteries are dead"
        elif(value > 4.45):
            return "batteries are full"
    if(device_id == 3):
        if(abs(value) > 90):
            return "the car is upside down"
    if(device_id == 4):
        if(value < 0):
            return "the car is going backwards"
        elif(value > 0):
            return "the car is going forwards"
        else:
            return "the car is standing still"
    return ""