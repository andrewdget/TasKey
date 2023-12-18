## NOTES ##
'''
1. implemented temprorary error handling, improve later
'''

## DEPENDENCIES ## 

from Utils import *


## DEFINITIONS ##

def ComPro(CurrentDB, input):
	'''
	DATABASE COMMANDS
	-n new task
	-e edit task
	-c complete task
	-d delete task
	-r restore task

	UI COMMANDS
	-i task info
	-m display main screen
	-a display archive screen
	-t switch tabs
	-k kill TasKey
	'''
	command_pairs = ComInt(input)
	if len(command_pairs.keys()) == 0:
		print('!!ERROR!! - CommandProcessor - line 31')
	else:
		leader = list(command_pairs.keys())[0]
		if leader == '-n':
			required_pairs = {'-n': 'req'}
			validation = ComValidation(command_pairs, required_pairs)
			if validation:
				CurrentDB.new(command_pairs)
			else:
				print('!!ERROR!! - CommandProcessor - line 40')

		elif leader == '-e':
			required_pairs = {'-e': 'req', '-n/-f/-c/-h/-m/-l/-d': 'opt'}
			validation = ComValidation(command_pairs, required_pairs)
			if validation:
				CurrentDB.edit(command_pairs)
			else:
				print('!!ERROR!! - CommandProcessor - line 48')

		elif leader == '-c':
			required_pairs = {'-c': 'req'}
			validation = ComValidation(command_pairs, required_pairs)
			if validation:
				CurrentDB.complete(command_pairs)
			else:
				print('!!ERROR!! - CommandProcessor - line 56')

		elif leader == '-d':
			required_pairs = {'-d': 'req'}
			validation = ComValidation(command_pairs, required_pairs)
			if validation:
				CurrentDB.delete(command_pairs)
			else:
				print('!!ERROR!! - CommandProcessor - line 64')

		elif leader == '-r':
			required_pairs = {'-r': 'req'}
			validation = ComValidation(command_pairs, required_pairs)
			if validation:
				CurrentDB.restore(command_pairs)
			else:
				print('!!ERROR!! - CommandProcessor - line 72')

		else:
			print('!!ERROR!! - CommandProcessor - line 75')



## EXECUTABLE ## 
