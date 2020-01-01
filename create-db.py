import sqlite3
import os
import config

print("Create database...")

db = sqlite3.connect(config.dbfilepath)
cur = db.cursor()
try:
	cur.execute("CREATE TABLE plantLog(datetime DATETIME NOT NULL, humidity FLOAT(7,2), temperature FLOAT(7,2), moisture FLOAT(7,2), waterlevel FLOAT(7,2), pumpstatus FLOAT(7,2));")
except:
	print("Table 'plantLog' already exists.")

db.close()

print("Database sucessfully created!")
