## NOTES ##
'''
- folder locations on windows need to have back slashes replaced with forward
	slashes

Bugs/Required Fixes:

To-Do:
- implement arrow-key scrolling
- implement save function (that doesn't require application to be closed/killed)


Future Features:
- add option for encrypting data
- internal settings configuration
- implement better "catch" system for a failed safesave
- internal tab creation
- add function for transferring tasks between tabs
- implement keyboard shortcut functionality (for calling application)

'''

## DEPENDENCIES ## 

from Interface import *
from FileManagement import *
from DataStructure import TaskDB

## DEFINITIONS ##

 
## EXECUTABLE ## 

version = 'v- 00.00.00 (Alpha2)'

exec(open('./Data/Paths.txt').read())
exec(open('./Data/Config.txt').read())

DBroster = BatchLoadDB(config, path_roster)

UI = TasKeyUI(version, config, DBroster, path_roster)

DBroster = UI.DBroster
BatchSafeSaveDB(DBroster, path_roster)
