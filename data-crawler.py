from __future__ import print_function 
import time
import sys
import sqlite3
import config

import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = '4'



try:
  humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
  moisture = 0
  waterlevel = 0
  pumpstatus = 0 

except:
  humidity = 0
  temperature = 0 
  moisture = 0
  waterlevel = 0
  pumpstatus = 0 
  datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
  f = open(config.alarmfilepath, 'a')
  alarm = "\n" + datetimeWrite + "-- Abfragefehler Arduino"
  f.write(alarm)
  f.close()
  

print("Write new data to database...",end="")
db = sqlite3.connect(config.dbfilepath)
cur = db.cursor()
datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))

sql_insert = ("""INSERT INTO plantLog (datetime,humidity,temperature,moisture,waterlevel,pumpstatus) VALUES (?,?,?,?,?,?)""",(datetimeWrite,humidity,temperature,moisture,waterlevel,pumpstatus))
cur.execute(*sql_insert)
db.commit()
db.close()
print("OK!")

print("Sucessfully finished all tasks!")
print(datetimeWrite)
