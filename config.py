##########################
# Config file
##########################

import platform

if platform.system() == "Linux":
    dbfilepath = "/home/pi/plantmonitor-db/plant.db"
    alarmfilepath = "/home/pi/alarm.txt"
    logfilepath = "/home/pi/plantmonitor-logs/"
    webserver = "Raspberry"
else:
    dbfilepath = "/Users/Martin/Desktop/plantmonitor/testdb/plant.db"
    alarmfilepath = "/Users/Martin/Desktop/plantmonitor/alarm.txt"
    webserver = "MacOSX"
