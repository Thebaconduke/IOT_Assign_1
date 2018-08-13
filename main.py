import os, sys, time
from pushbullet import send_data
from datetime import datetime
from sense_hat import SenseHat
import sqlite3 as lite

dbname='sensehat.db'
sampleFreq = 1 # time in seconds

def createDatabase():
	con = lite.connect('sensehat.db')
	with con: 
		cur = con.cursor() 
		cur.execute("CREATE TABLE IF NOT EXISTS SENSEHAT_data(timestamp DATETIME, temp NUMERIC, hum Numeric)")

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(float(res.replace("temp=","").replace("'C\n","")))
	
def push_Bullet(temp):
    if temp < 20:
        send_data()
    else:
        print("Don't need sweater")
		
# get data from SenseHat sensor
def getSenseHatData():	
	sense = SenseHat()
	temp = sense.get_temperature()
	hum = sense.get_humidity()
	temp = temp - ((getCPUtemperature() - temp)/1)
	if temp is not None:
		temp = round(temp, 1)
		hum = round(hum,1)
		logData (temp,hum)
		push_Bullet(temp)

# log sensor data on database
def logData (temp,hum):	
    conn=lite.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO SENSEHAT_data values((?), (?), (?))", (datetime.now(), temp,hum,))
    conn.commit()
    conn.close()

# display database data
def displayData():
    conn=lite.connect(dbname)
    curs=conn.cursor()
    print ("\nEntire database contents:\n")
    for row in curs.execute("SELECT * FROM SenseHat_data"):
        print (row)
    conn.close()

# main function
def main():
	createDatabase()
	for i in range (0,3):
		getSenseHatData()
		time.sleep(sampleFreq)
	displayData()

# Execute program 
main()
