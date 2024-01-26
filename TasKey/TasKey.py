## NOTES ##
'''
Bugs/Required Fixes:
- validation of date input is incomplete, sometimes results in strings
- add feature which allows task to be completely deleted (from archive)
- prompt protect doesn't function as well as desired, look at improving

To-Do:
- implement arrow-key scrolling
- implement keyboard shortcut functionality (for calling application)
- implement save function (that doesn't require application to be closed/killed)
- make note that shared folder locations on windows need to have paths with "/"
- add ability to transfer tasks between tabs
- add a no deadline task

Future Features:
- add option for encrypting data
- internal settings configuration
- implement better "catch" system for a failed safesave
- internal tab creation
- add function for transferring tasks between tabs

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
