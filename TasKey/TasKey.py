## NOTES ##
'''
Required Fixes:
1. paths to shared folders load but do not save
2. implement functioning progress bars
3. inputting erroneous tab name results in frozen command line.
4. need to improve input error handling so the program continues to work
5. using "-" in task name, etc. causes issues
6. holding backspace may still delete prompt on windows machine
7. need to make date formats consistent with one another


To-Do:
1. need to add validation function for "Paths.txt"/"Config.txt" files
2. implement keyboard shortcut(s) functionality
3. update application icon
5. implement a force-save function
6. internal settings configuration, tab creation, etc.
7. implement arrow key scrolling
8. improve/clean up the ASCII_ProgressBar function
9. add option for encrypting data
11. make not that shared folder locations on windows need to have paths
	with "/"


Ideas:
1. add ability to transfer tasks between tabs
2. add a no deadline task
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

UI = TasKeyUI(version, config, DBroster)

DBroster = UI.DBroster
# BatchSafeSaveDB(DBroster)
