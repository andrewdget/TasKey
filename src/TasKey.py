## NOTES ##
'''
1. need to add validation function for "Paths.txt"/"Config.txt" files
'''

## DEPENDENCIES ## 

from Interface import *
from DataStructure import TaskDB

## DEFINITIONS ##


## EXECUTABLE ## 

version = 'v- 00.00.00 (Beta)'

exec(open('./Data/Paths.txt').read())
exec(open('./Data/Config.txt').read())

temp_db = TaskDB(config, 'temp_db', './dummy/path')

TasKeyUI(version, config, temp_db, paths)
