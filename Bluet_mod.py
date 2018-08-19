#!/usr/bin/env python3
import bluetooth,os,time,sys,string
from main import getTemp
from databaseMod import *
from sense_hat import SenseHat
from pushbullet import push_notification

translator = str.maketrans('', '', string.punctuation)

# start function
def start():
	if len(sys.argv) > 1:
		user_name, device_name = sys.argv[1].translate(translator), sys.argv[2].translate(translator)
		insertUser(user_name,device_name,"")
		print("User inserted into database, please run again to start program unless cron is running")
	else:
		search()

# Search for device using device name
def search():
	found = False
	while True:
		deviceList = displayData("USER_data")
		currDevice = None
		nearby_devices = bluetooth.discover_devices()
		
		for mac_address in nearby_devices:
			for device in deviceList:
				if device is not None and bluetooth.lookup_name(
				mac_address, timeout=5) is not None:
					
					deviceName = device[2].translate(translator)
					if deviceName == bluetooth.lookup_name(
					mac_address, timeout=5).translate(translator):
						currDevice = device
						macUpdate(mac_address,device[2])
						break
			else:
				continue
			break
		
		#If device found display greeting with temp and send message via pushbullet
		if currDevice is not None:
			if found == False:
				found = True
				sense = SenseHat()
				sense.set_rotation(180)
				temp = getTemp()
				blue = (0, 0, 255)
				yellow = (255, 255, 0)
				sense.show_message("Hi {}! Current Temp is {}*c".format(
				currDevice[1], temp), scroll_speed=0.1, text_colour=yellow, 
				back_colour=blue)
				hello_u = "Hello {}".format(currDevice[1])
				current_temp = "The Current Temperature is {}°c".format(temp)
				push_notification(hello_u, current_temp)
				sense.clear()
		else:
			found = False
#Execute
start()
