#!/usr/bin/env python3
import bluetooth
import os
import time
from sense_hat import SenseHat
from pushbullet import push_notification

# start function
def start():
    user_name = input("Enter your name: ")
    device_name = input("Enter the name of your phone: ")
    search(user_name, device_name)

#CPU temp function
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(float(res.replace("temp=","").replace("'C\n","")))

# Search for device using device name
def search(user_name, device_name):
    while True:
        device_address = None
        dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
        print("\nCurrently: {}".format(dt))
        time.sleep(3) #Sleep 3 seconds 
        nearby_devices = bluetooth.discover_devices()

        for mac_address in nearby_devices:
            if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                device_address = mac_address
                break
        #If device found display greeting with temp and send message via pushbullet
        if device_address is not None:
            sense = SenseHat()
            temp = round(sense.get_temperature() - (getCPUtemperature() - sense.get_temperature()))
            blue = (0, 0, 255)
            yellow = (255, 255, 0)
            sense.show_message("Hi {}! Current Temp is {}*c".format(user_name, temp), scroll_speed=0.1, text_colour=yellow, back_colour=blue)
            hello_u = "Hello {}".format(user_name)
            current_temp = "The Current Temperature is {}°c".format(temp)
            push_notification(hello_u, current_temp)
            sense.clear()
        else:
            print("Can't find specified device")

#Execute
start()
