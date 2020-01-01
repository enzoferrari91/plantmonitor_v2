##########################
# Config file
##########################

import platform

if platform.system() == "Linux":
    dbfilepath = "/home/pi/plantmonitor_v2-db/plant.db"
    alarmfilepath = "/home/pi/alarm.txt"
    logfilepath = "/home/pi/plantmonitor_v2-logs/"
    webserver = "Raspberry"
else:
    dbfilepath = "/Users/Martin/Desktop/Python/plantmonitor_v2/testdb/plant.db"
    alarmfilepath = "/Users/Martin/Desktop/Python/plantmonitor_v2/alarm.txt"
    webserver = "MacOSX"
