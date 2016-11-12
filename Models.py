import sqlite3 as sql
import urllib2
import json
from datetime import datetime, timedelta

database = "Building.db"

def insert_data():
	response = urllib2.urlopen('https://my.engr.illinois.edu/labtrack/util_data_json.asp')
	data = response.read()
	data = json.loads(data)['data']

	with sql.connect(database) as con:
	    cur = con.cursor()
	    year = datetime.now().year
	    month = datetime.now().month
	    day = datetime.now().day
	    hour = datetime.now().hour
	    for lab in data:
	    	lab_name = ' '.join(lab['strlabname'].split(' ')[1:])
	    	if lab_name == '':
	    		lab_name = 'default'
	    	cur.execute("INSERT INTO Labs (LabName, InUse, Total, Year, Month, Day, Hour) VALUES (?,?,?,?,?,?,?)", (lab_name, lab['inusecount'], lab['machinecount'], year, month, day, hour))
	    con.commit()

def get_historical_data(lab_name):
	total = 0
	num = 0
	average = [-1] * 24

	for j in range(0, 24):
		for i in range(0, 4):
			d = datetime.today() + timedelta(hours=j) - timedelta(days=7*(i+1))
			with sql.connect(database) as con:
				cur = con.cursor()
				result = cur.execute("SELECT InUse FROM Labs WHERE LabName = (?) AND Year = (?) AND Month = (?) AND Day = (?) AND Hour = (?);", (lab_name, d.year, d.month, d.day, d.hour))
				con.commit()
			result = result.fetchall()
			if (len(result) > 0):
				total += result[0][0]
				num += 1

		if num > 0:
			average[j] = total / num
		else:
			print('No historical data available')

	return average
	

# insert_data()
get_historical_data('4th Floor Center')