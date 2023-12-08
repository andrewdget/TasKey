## NOTES ##
'''

'''

## DEPENDENCIES ## 
import pyfiglet
import datetime

## DEFINITIONS ##


## EXECUTABLE ## 

current = datetime.datetime.now()

hour = str(current.hour)
if len(hour) == 1:
	hour = '0' + hour

minute = str(current.minute)
if len(minute) == 1:
	minute = '0' + minute


weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weekday = weekdays[current.weekday()]

day = str(current.day)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month = months[current.month - 1] # -1 added due to 0 based indexing

year = str(current.year)


datetime_str = hour+':'+minute +'   '+ weekday+'\n' + month+' ' +day+' ' + year

ASCII_datetime = pyfiglet.figlet_format(datetime_str, font='smslant')
print(ASCII_datetime)



