## NOTES ##
'''
Required Fixes:
1. inputing erronous tab name results in frozen command line.
2. need to improve input error handling so the program continues to work
3. using "-" in task name, etc. causes issues
4. check if days remaining fix, fixed issue with manual deadlines not
	effecting priority score. 
5. holding backspace may still delete prompt on windows machine


To-Do:
1. need to add validation function for "Paths.txt"/"Config.txt" files
2. implement keyboard shortcut(s) functionality
3. update application icon
4. disable case sensitivity for tab names (make option in config)
5. implement a force-save function
6. internal settings configuration, tab creation, etc.
7. implement arrow key scrolling
8. implement functioning progress bars
 

Ideas:
1. add ability to transfer tasks between tabs
2. no deadline task
3. 
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
BatchSafeSaveDB(DBroster)
