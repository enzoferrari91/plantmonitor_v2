from __future__ import print_function 
import serial
import time
import sys
import sqlite3
import config

serialArduino = '/dev/ttyACM0' # Serial port for Arduino


def send(port, bytes, tr): 
  port.write(bytes)
  time.sleep(tr)
  

def readArduino(msg):
  print ("Open serial port /dev/tty/ACM0...", end="")
  Arduino=serial.Serial(port=serialArduino, baudrate=9600)
  time.sleep(2)

  send(Arduino, msg, 0.5)
  print("Ready to receive...",end="")

  data=""
  c = Arduino.read()
  while c != "!":
    data = data + c
    c = Arduino.read()
    
  print("Result OK!")
  data = data.split(";")
  data_list = [float(i) for i in data]
  return(data_list)

try:
  print("Starting communication!")
  print("ARDUINO...",end="")
  data_list = readArduino("?")
  
  humidity = data_list[0]
  temperature = data_list[1] 
  moisture = data_list[2]
  waterlevel = data_list[3]
  pumpstatus = data_list[4]

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
