from flask import Flask, render_template, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

lastReadTime = None

@app.route('/logs', methods=['GET'])
def metrics():  
	try:
		global lastReadTime
		this_log = []
		with open('clinics.log', "r") as logFile:
			lines = logFile.readlines()
			# iterate over lines in reversed order (most recent first)
			# of entries in the monitored time frame
			i = 1
			while i < len(lines) :
				log = lines[i].split(' - ')
				time = datetime.strptime(log[0], "%d/%b/%Y:%H:%M:%S")
				if lastReadTime == None or time >= lastReadTime:
					this_log.append(log)
				i += 1
		now = datetime.now()
		lastReadTime = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
		print(len(this_log))
		return json.dumps(this_log)
	except Exception as e:
		print(e)
		return ""
	

@app.route('/', methods=['GET'])
def index():  
	return render_template('index.html')

if __name__ == '__main__':
	app.run()
