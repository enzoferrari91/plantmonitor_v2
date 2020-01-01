from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import g
from flask import jsonify

import sqlite3
import time
from datetime import datetime, timedelta
import config

# FLASK APP
app = Flask(__name__)

def extracttime(s):
  start = s.index(" ")
  return s[(start+1):(start+6)]

def extractdate(s):
	end = s.index(" ")
	return s[:end]

# Get current date (e.g. 2015-11-20)
def getDateToday():
	dateToday = time.strftime("%Y-%m-%d")
	return(dateToday)

# Get tommorow's date
def getDates(dateDB):
	dateToday = datetime.strptime(dateDB,"%Y-%m-%d") # Type 'Datetime'
	dateTomorrow = dateToday + timedelta(days=1) 	 # Type 'Datetime'
	dateTomorrow = datetime.strftime(dateTomorrow,"%Y-%m-%d")	# Type 'String'

	return(dateTomorrow)


# Get power data from SQLite3
def selectPlantDB(date_from_DB, date_to_DB):
	cur = g.db.cursor()
	cur.execute("SELECT * FROM plantLog WHERE datetime >= ? and datetime < ?", (date_from_DB, date_to_DB))
	data = cur.fetchall()

	# Create lists
	humidity = list(zip(*data)[1])
	temperature = list(zip(*data)[2])
	moisture = list(zip(*data)[3])
	waterlevel = list(zip(*data)[4])
	pumpstatus = list(zip(*data)[5])
	timestampList = list(zip(*data)[0])
	timestampList = [str(x) for x in timestampList]
	timestampList = [extracttime(x) for x in timestampList]
		
	# Return the lists
	return (humidity, temperature, moisture, waterlevel, pumpstatus, timestampList)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/system_messages")
def system_messages():
	return render_template("system_messages.html")

@app.route("/msg/<msg>")
def msg(msg):
	f = open((config.logfilepath + msg) , 'r')
	s = f.read()
	f.close()
	return(s)

@app.route("/alarmprotokoll")
def alarmprotokoll():
	f = open(config.alarmfilepath, 'r')
	s = f.read()
	s=s.replace ('\n', '<br>')
	f.close()
	return(s)

@app.route("/_get_data")
def showtimeseriesJSON():
    date_from_DB = request.args.get('dateselect_from')
    date_to_DB = request.args.get('dateselect_to')

    date_to_DB = getDates(date_to_DB)

    try:
    	humidity, temperature, moisture, waterlevel, pumpstatus, timestampList = selectPlantDB(date_from_DB,date_to_DB)
    	humidity = [0 if x is None else x for x in humidity]
    	temperature = [0 if x is None else x for x in temperature]
    	moisture = [0 if x is None else x for x in moisture]
    	waterlevel = [0 if x is None else x for x in waterlevel]
    	pumpstatus = [0 if x is None else x for x in pumpstatus]

    	actual_humidity = humidity[-1]
    	actual_temperature = temperature[-1]
    	actual_moisture = moisture[-1] # last entry in list
    	actual_waterlevel = waterlevel[-1]
    	actual_pumpstatus = pumpstatus[-1]

    	humidity.extend((288-len(humidity))*[0])
    	temperature.extend((288-len(temperature))*[0])
    	moisture.extend((288-len(moisture))*[0])
    	waterlevel.extend((288-len(waterlevel))*[0])
    	pumpstatus.extend((288-len(pumpstatus))*[0])
    	timestampList.extend((288-len(timestampList))*[""])

    except:
    	humidity = []
    	temperature = []
    	moisture = []
    	waterlevel = []
    	pumpstatus = []
    	timestampList = []

    	actual_humidity = 0
    	actual_temperature = 0
    	actual_moisture = 0
    	actual_waterlevel = 0
    	actual_pumpstatus = 0


    return jsonify(humidity=humidity,
    	temperature=temperature,
    	moisture=moisture,
    	waterlevel=waterlevel,
    	pumpstatus=pumpstatus,
    	actual_humidity=actual_humidity, actual_temperature=actual_temperature,
    	actual_moisture=actual_moisture, actual_waterlevel=actual_waterlevel,
    	actual_pumpstatus=actual_pumpstatus,
    	timestampList=timestampList)	
    
@app.before_request
def before_request():
	g.db = sqlite3.connect(config.dbfilepath)

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()

if __name__ == "__main__":
	if config.webserver == "MacOSX":
		app.run(host='0.0.0.0', debug=True)
	if config.webserver == "Raspberry":
		app.run(host='0.0.0.0', port=80)

