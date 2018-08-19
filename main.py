#!/usr/bin/env python3
import os, sys, time
from databaseMod import *
from pushbullet import send_data
from sense_hat import SenseHat

sense = SenseHat()

# Get the CPU temperature
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(float(res.replace("temp=","").replace("'C\n","")))

def getTemp():
	temp = None
	temp = sense.get_temperature()
	temp = round(temp - ((getCPUtemperature() - temp)/1.34))
	return temp

# If push bullet below 20 degrees activate a pushbullet 	
def push_Bullet(temp):
    if temp < 20:
        send_data()
    else:
        print("Don't need sweater")

# get Temperature, and humidity data from SenseHat sensor
def getSenseHatData():
	hum = sense.get_humidity()
	temp = getTemp()
	
	if temp is not None:
		temp,hum = round(temp, 1),round(hum,1)
		insertTemp(temp,hum)
		push_Bullet(temp)

# main function
def main():
	createDatabase()
	getSenseHatData()
	getTemp =  displayData()
	for data in getTemp:
		print(data)

# Execute Main (program)
if __name__ == "__main__":
	main()
