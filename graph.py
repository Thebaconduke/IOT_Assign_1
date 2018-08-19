#!/usr/bin/env python3
from flask import Flask, render_template,g
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = '/home/pi/A1_proto/sensehat.db'
#Connect Database
def get_db():
	db = getattr(g,'_database',None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db
	 
@app.teardown_appcontext
def close_connection (exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route('/js/<path:path>')
def send_js(path): return send_from_directory('js', path)

def query_db(query, args = (), one = False):
	cur = get_db().execute (query, args)
	rv = cur.fetchall()
	cur.close
	return (rv[0] if rv else None) if one else rv
	
# Select statment which allows us to view the data on the webpage.
@app.route("/")
def index():
	timestamp,temp,hum = [],[],[]
	for sense in query_db ('SELECT * FROM SENSEHAT_data'):
		timestamp.append(str(sense[1])[:-10])
		temp.append ( str(sense[2]) )
		hum.append ( str(sense[3]) )

	templateData = {
	'timestamp' : timestamp,
	'temp' : temp,
	'hum' : hum
	}
	return render_template('Graph.html', **templateData)

if __name__ == "__main__":
   app.run(host='192.168.1.31', port=8080, debug=True)






