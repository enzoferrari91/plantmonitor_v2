from __future__ import print_function 
import time

print("Cron test...",end="")
datetimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
print(datetimeWrite,end="")
print("...OK!")
