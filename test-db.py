import sqlite3
import time
import random
import config

db = sqlite3.connect(config.dbfilepath)

cur = db.cursor()

dateToday = time.strftime("%Y-%m-%d ")

cur.execute("SELECT * FROM plantLog WHERE datetime LIKE ?", (dateToday+'%' ,))

data = cur.fetchall()
humidity = list(zip(*data)[1])
temperature = list(zip(*data)[2])
moisture = list(zip(*data)[3])
waterlevel = list(zip(*data)[4])
pumpstatus = list(zip(*data)[5])
timestampList = list(zip(*data)[0])

print humidity
print temperature
print moisture
print waterlevel
print pumpstatus
print timestampList

db.close()
