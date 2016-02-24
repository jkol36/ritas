import pytz
import time
from datetime import datetime, timedelta
from dateutil import tz

storeZone = pytz.timezone('America/Los_Angeles')
myZone = tz.tzlocal()#pytz.timezone('America/New_York')

storeStartTime = datetime.now(storeZone)
myStartTime = datetime.now(myZone)

storeSeconds = time.mktime(storeStartTime.timetuple())
mySeconds = time.mktime(myStartTime.timetuple())
differenceInSeconds = int(storeSeconds - mySeconds)

storeStartTime = storeStartTime.replace(day=18, hour=0, minute=0, second=0)
storeEndTime = storeStartTime.replace(day=18, hour=23, minute=59, second=59)

storeStartTimeInSeconds = int(storeStartTime.strftime("%s")) - differenceInSeconds #MULTIPLE BY 1000.0 for MILLISECONDS
storeEndTimeInSeconds = int(storeEndTime.strftime("%s")) - differenceInSeconds

print("START: " + str(storeStartTimeInSeconds) + "\tEND: " + str(storeEndTimeInSeconds))

clientCreatedTime = 1455837456000 / 1000.0
clientCreatedTime = clientCreatedTime + differenceInSeconds
storeTime = datetime.fromtimestamp(clientCreatedTime) 
print(storeTime)

timeFormat = "%Y-%m-%dT%H:%M:%S";
print(storeTime.strftime(timeFormat))
