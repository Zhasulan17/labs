# 1
from datetime import datetime,timedelta
today = datetime.today()
newdate = today - timedelta(days = 5)
print (newdate.strftime("%d-%m-%Y"))


# 2
from datetime import datetime,timedelta
today = datetime.today()
yesterday = today - timedelta(days = 1)
tomorrow = today + timedelta(days = 1)
print (yesterday.strftime("%d-%m-%Y"))
print (today.strftime("%d-%m-%Y"))
print (tomorrow.strftime("%d-%m-%Y"))


# 3
from datetime import datetime,timedelta
now = datetime.now()
x = now.replace(microsecond = 0)
print (x)


# 4
from datetime import datetime,timedelta
date1 = datetime(2025, 2, 10, 12, 0, 0)
date2 = datetime(2025, 2, 14, 15, 30, 0)

difference_in_seconds = abs((date2 - date1).total_seconds())
print("Difference between two dates in seconds:", difference_in_seconds)





















