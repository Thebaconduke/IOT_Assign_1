from flask import Flask, render_template,g
import sqlite3
app = Flask(name)
DATABASE = 'sensehat.db'

def get_db():
	db = getattr(g,'_database',None)
	if db is None:
		db = g._database = sqlite3.connect[DATABASE]
		return db
	 
@app.teardown_appcontext
def close_connection (exception)
	db = getattr(g, '_database",None)
	if db is not None
		db.close()

def query_db(query, args = (), one = false):
	cur = get_db().execute (query, args)
	rv = cur.fetchall()
	cur.close
	return (rb[0] if rv else None) if one else rv

@app.route("/")
def index():
	timestamp,temp,hum = []
	for sense in query_db ('SELECT * FROM Senesehat_data'):
		timestamp.append(sense ['timestamp'])
		timestamp.append (sense ['temp'] )
		timestamp.append (sense ['hum'] )

	templateData = (
	'timestamp' : timestamp,
	'temp' : temp,
	'hum' : hum
	)
	return render_templates ('Demo_graph.html', **templateData)

if name == "main":
	app.run(host='0.0.0.0', port=80 debug=True)






