# cron.py
import datetime
import pytz

weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
tz_AR = pytz.timezone('America/Argentina/Buenos_Aires') 
datetime_AR = datetime.datetime.now(tz_AR)
if datetime_AR.weekday() < 4:
    if datetime_AR.hour >= 10 and datetime_AR.hour <= 16: # Horario Bancario
        exec(open("main.py").read())

