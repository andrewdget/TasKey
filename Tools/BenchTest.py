## NOTES ##
'''

'''

## DEPENDENCIES ## 
import tkinter as tk
import tkinter.font as tkf
import pyfiglet
import datetime

from CommandProcessor import *
from DataStructure import *

## DEFINITIONS ##


## EXECUTABLE ## 

exec(open('./Data/Paths.txt').read())
exec(open('./Data/Config.txt').read())

newDB = TaskDB(config, 'test', 'nothing')

input_text = '-n this is a test task'
ComPro(newDB, input_text)

input_text = '-e aa -n renamed'
ComPro(newDB, input_text)

input_text = '-d aa'
ComPro(newDB, input_text)

input_text = '-r aa'
ComPro(newDB, input_text)

print(newDB.Active[0].name)

