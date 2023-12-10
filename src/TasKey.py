## NOTES ##
'''
1. need to add validation function for "Paths.txt"/"Config.txt" files
'''

## DEPENDENCIES ## 

from Interface import *

## DEFINITIONS ##


## EXECUTABLE ## 

version = 'v- 00.00.00 (Beta)'

exec(open('./Data/Paths.txt').read())
exec(open('./Data/Config.txt').read())

TasKeyUI(version, config, paths)
