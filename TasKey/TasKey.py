## NOTES ##
'''
- folder locations on windows need to have back slashes replaced with forward
	slashes

Bugs/Required Fixes:
- when viewing additional information, priority should have first letter
	capitalized
- implement capitalization agnostic flags/alpha indices
	* Accidentally using a uppercase flag can result in unintentionally not
		accepting a follower flag/pair in a way that is not obvious to the user
		(as a default gets used instead)
- when trying to eliminate a footnote or a deadline, DataStructure.py is expects
	```None``` rather than string.
- one can "complete" already completed tasks which results in a duplicate of the
	task being added to the archive DB. May occur with other commands such as
	restoring already active tasks.
- when editing task deadline/priority, progress bars dont seem to always update
	right away. 

To-Do:
- Create setting that allows TasKey font size to be adjusted.

Future Features:
- add option for encrypting data
- internal settings configuration
- implement better "catch" system for a failed safesave
- internal tab creation
- add function for transferring tasks between tabs
- implement keyboard shortcut functionality (for calling application)
- database refreshing (for use with shared databases)
- more robust save/load location error handling and ability to change save
	location while in operation

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
