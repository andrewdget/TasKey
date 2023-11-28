## NOTES ##
'''
1. Need to create settings & file management functions/module.
'''

## DEPENDENCIES ##
from UIFunctions import *


## WORKING SPACE ##

settings = {
	'Mon': True,
	'Tue': True,
	'Wed': True,
	'Thu': True,
	'Fri': True,
	'Sat': False,
	'Sun': False,
	'HPeriod': 1,
	'MPeriod': 2,
	'LPeriod': 3
	}

root = tk.Tk()
TasKeyUI(root, settings)
root.mainloop()



