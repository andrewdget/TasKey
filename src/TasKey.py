## NOTES ##
'''
1. need to add validation function for "Paths.txt"/"Config.txt" files
'''

## DEPENDENCIES ## 

from Interface import *
from FileManagement import *
from DataStructure import TaskDB

## DEFINITIONS ##

 
## EXECUTABLE ## 

version = 'v- 00.00.00 (Alpha)'

exec(open('./Data/Paths.txt').read())
exec(open('./Data/Config.txt').read())

DBroster = BatchLoadDB(config, path_roster)

UI = TasKeyUI(version, config, DBroster)

DBroster = UI.DBroster
BatchSafeSaveDB(DBroster)
