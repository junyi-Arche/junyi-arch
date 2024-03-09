import datetime
import time
timedate = '1970-09-01 08:00'
timeStamp = 1689510691
timeArray = datetime.datetime.fromtimestamp(timeStamp)
print(timeArray)
times = datetime.datetime.strptime(timedate, '%Y-%m-%d %H:%M').timestamp()
print(times)