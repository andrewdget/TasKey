## NOTES ##
'''
Required Fixes:
1. paths to shared folders load but do not save
3. inputting erroneous tab name results in frozen command line.
4. need to improve input error handling so the program continues to work
5. using "-" in task name, etc. causes issues
6. holding backspace may still delete prompt on windows machine


To-Do:
1. note TasKey displays dates in diff format than expected Str2Date function 
	date input format... will lead to confusion. Suggest finding fix. 
2. need to add feature that eliminates any bad (temp) saves
3. need to add validation function for "Paths.txt"/"Config.txt" files
4. implement keyboard shortcut(s) functionality
5. implement a force-save function
6. internal settings configuration, tab creation, etc.
7. implement arrow key scrolling
8. add option for encrypting data
9. make not that shared folder locations on windows need to have paths with "/"
10. add ability to transfer tasks between tabs
11. add a no deadline task
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
