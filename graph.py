from flask import Flask, render_template,g
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'sensehat.db'

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

@app.route("/")
def index():
	timestamp,temp,hum = [],[],[]
	for sense in query_db ('SELECT * FROM SENSEHAT_data'):
		timestamp.append(str(sense[0])[:-10])
		temp.append ( str(sense[1]) )
		hum.append ( str(sense[2]) )

	templateData = {
	'timestamp' : timestamp,
	'temp' : ",".join(temp),
	'hum' : ",".join (hum)
	}
	return render_template('Demo_graph.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)






