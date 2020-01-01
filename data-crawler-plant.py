from __future__ import print_function 
import serial
import time
import sys
import sqlite3
#import config

#serialArduino = '/dev/ttyACM0' # Serial port for Arduino
serialArduino = '/dev/tty.usbmodemfa131'

def send(port, bytes, tr): 
  port.write(bytes)
  time.sleep(tr)
  

def readArduino(msg):
  print ("Open serial port /dev/tty/ACM0...", end="")
  Arduino=serial.Serial(port=serialArduino, baudrate=9600)
  time.sleep(2) #2

  send(Arduino, msg, 0.5)
  print("Ready to receive...",end="")

  data=""
  c = Arduino.read()
  while c != "!":
    data = data + c
    c = Arduino.read()
    
  print("Result OK!")
  return data

try:
  print("Starting communication!")
  print("ARDUINO...",end="")
  #power_pv = readArduino("?")   # W
  #if power_pv < 70:             # Threshold for Power
  #  power_pv = 0
  text = readArduino("?")
  print(text)

except:
  #power_pv = 0
  #datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
  print("Error)")

  #f = open(config.alarmfilepath, 'a')
  #alarm = "\n" + datetimeWrite + "-- Abfragefehler Arduino"
  #f.write(alarm)
  #f.close()
  

#print("Write new data to database...",end="")
#db = sqlite3.connect(config.dbfilepath)
#cur = db.cursor()
#datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))

#sql_insert = ("""INSERT INTO powerLog (datetime,power_bez,power_einsp,power_pv) VALUES (?,?,?,?)""",(datetimeWrite,power_bez,power_einsp,power_pv))
#cur.execute(*sql_insert)
#db.commit()
#db.close()
#print("OK!")

#print("Sucessfully finished all tasks!")
#print(datetimeWrite)





