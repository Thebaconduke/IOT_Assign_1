import sqlite3 as lite
from datetime import datetime

dbname='/home/pi/A1_proto/sensehat.db'

def createDatabase():
	con = lite.connect(dbname)
	with con: 
		cur = con.cursor() 
		cur.execute("CREATE TABLE IF NOT EXISTS SENSEHAT_data"+
		"(temp_id INTEGER PRIMARY KEY AUTOINCREMENT,timestamp DATETIME,"+
		" temp NUMERIC, hum Numeric)")
		cur.execute("CREATE TABLE IF NOT EXISTS USER_data"+
		"(user_id INTEGER PRIMARY KEY AUTOINCREMENT,username STRING,"+
		"name STRING, macAddr STRING)")
		
def insertTemp (temp,hum):	
    sendQuery ("INSERT INTO SENSEHAT_data (timestamp,temp,hum) "+
	"VALUES('{}', '{}', '{}')".format(datetime.now(),temp,hum))

def insertUser (username,name,macAddr):	
    sendQuery ("INSERT INTO USER_data (username, name,macAddr) "+
	"VALUES('{}', '{}', '{}')".format(username,name,macAddr))

def macUpdate (macAddr,name):
    sendQuery ("UPDATE USER_data SET macAddr = '{}' WHERE name = '{}'"+
	"".format(macAddr,name))

def sendQuery(query):
	conn=lite.connect(dbname)
	curs=conn.cursor()
	curs.execute(query)
	conn.commit()
	conn.close()
	
def displayData(tableName = "SenseHat_data", last=False):
	rowsList = []
	conn=lite.connect(dbname)
	curs=conn.cursor()
	if last:
		query = "SELECT * FROM {} ORDER BY temp_id DESC LIMIT "
		query =+"48 ".format(tableName)
	else:
		query = "SELECT * FROM {}".format(tableName)
	for row in curs.execute(query):
		rowsList.append(row)
	conn.close()	
	return rowsList
