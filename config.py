##########################
# Config file
##########################

import platform

if platform.system() == "Linux":
    dbfilepath = "/home/pi/plantmonitor-db/plant.db"
    #apifilepath = "/home/pi/planetosAPI.txt"
    #zstfilepath = "/home/pi/tempzst.txt"
    alarmfilepath = "/home/pi/alarm.txt"
    logfilepath = "/home/pi/plantmonitor-logs/"
    webserver = "Raspberry"
else:
    dbfilepath = "/Users/Martin/Desktop/plantmonitor/testdb/plant.db"
    #apifilepath = "/Users/martinlenz/Desktop/Python/plantmonitor/planetosAPI.txt"
    alarmfilepath = "/Users/Martin/Desktop/plantmonitor/alarm.txt"
    webserver = "MacOSX"

# Zwettl
#lat = 48.50
#lon = 15.25
