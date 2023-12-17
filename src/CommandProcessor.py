## NOTES ##
'''
1. implemented temprorary error handling, improve later
'''

## DEPENDENCIES ## 

from Utils import *


## DEFINITIONS ##

def ComPro(TaskDB, input):
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
	leader = list(command_pairs.keys())[0]
	if leader == '-n':
		required_pairs = {'-n': 'req'}
		validation = ComValidation(command_pairs, required_pairs)
		if validation:
			TaskDB.new(command_pairs)
		else:
			print('!!ERROR!! - CommandProcessor - line 38')

	elif leader == '-e':
		required_pairs = {'-e': 'req', '-n/-f/-c/-h/-m/-l/-d': 'opt'}
		validation = ComValidation(command_pairs, required_pairs)
		if validation:
			TaskDB.edit(command_pairs)
		else:
			print('!!ERROR!! - CommandProcessor - line 46')

	elif leader == '-c':
		required_pairs = {'-c': 'req'}
		validation = ComValidation(command_pairs, required_pairs)
		if validation:
			TaskDB.complete(command_pairs)
		else:
			print('!!ERROR!! - CommandProcessor - line 54')

	elif leader == '-d':
		required_pairs = {'-d': 'req'}
		validation = ComValidation(command_pairs, required_pairs)
		if validation:
			TaskDB.delete(command_pairs)
		else:
			print('!!ERROR!! - CommandProcessor - line 62')

	elif leader == '-r':
		required_pairs = {'-r': 'req'}
		validation = ComValidation(command_pairs, required_pairs)
		if validation:
			TaskDB.restore(command_pairs)
		else:
			print('!!ERROR!! - CommandProcessor - line 70')

	else:
		print('!!ERROR!! - CommandProcessor - line 73')



## EXECUTABLE ## 
