## NOTES ##
'''
1. -i command has no validation to insure alpha index given is valid
2. -t command has no validation to insure commanded tab exists

'''

## DEPENDENCIES ## 

from Utils import *


## DEFINITIONS ##

def ComPro(DBroster, current_tab, input_str):
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
	DB = DBroster[current_tab]
	if len(input_str) > 0: # bypasses command processor if no input is given
		command_pairs = ComInt(input_str)
		if len(command_pairs.keys()) == 0:
			target = 'msg'
			command = 'ERROR: no flags given'
		else:
			leader = list(command_pairs.keys())[0]
			if leader == '-n':
				required_pairs = {'-n': 'req'}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					try:
						DB.new(command_pairs)
					except:
						target = 'msg'
						command = 'ERROR: new task command contains invalid elements'
				else:
					target = 'msg'
					command = 'ERROR: new task command missing elements'

			elif leader == '-e':
				required_pairs = {'-e': 'req', '-n/-f/-c/-h/-m/-l/-d': 'opt'}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					try:
						DB.edit(command_pairs)
					except:
						target = 'msg'
						command = 'ERROR: edit task command contains invalid elements'
				else:
					target = 'msg'
					command = 'ERROR: edit task command missing elements'

			elif leader == '-c':
				required_pairs = {'-c': 'req'}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					try:
						DB.complete(command_pairs)
					except:
						target = 'msg'
						command = 'ERROR: complete task command contains an invalid index'
				else:
					target = 'msg'
					command = 'ERROR: complete task command missing index'

			elif leader == '-d':
				required_pairs = {'-d': 'req'}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					try:
						DB.delete(command_pairs)
					except:
						target = 'msg'
						command = 'ERROR: delete task command contains an invalid index'
				else:
					target = 'msg'
					command = 'ERROR: delete task command missing index'

			elif leader == '-r':
				required_pairs = {'-r': 'req'}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					try:
						DB.restore(command_pairs)
					except:
						target = 'msg'
						command = 'ERROR: restore task command contains an invalid index'
				else:
					target = 'msg'
					command = 'ERROR: restore task command missing index'

			elif leader == '-i':
				required_pairs = {'-i': 'req'}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					index = command_pairs['-i']
					if len(index) == 2 and index.islower() and index.isalpha():
						target = 'sel'
						command = index
					elif index == 'None':
						target = 'sel'
						command = None
					else:
						target = 'msg'
						command = 'ERROR: information command contains an invalid index'
				else:
					target = 'msg'
					command = 'ERROR: information command missing index'

			elif leader == '-m':
				required_pairs = {'-m': None}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					target = 'win'
					command = 'Active'
				else:
					target = 'msg'
					command = 'ERROR: switch to main command provided invalid elements'

			elif leader == '-a':
				required_pairs = {'-a': None}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					target = 'win'
					command = 'Archive'
				else:
					target = 'msg'
					command = 'ERROR: switch to archive command provided invalid elements'	

			elif leader == '-t':
				required_pairs = {'-t': 'req'}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					if command_pairs['-t'] in list(DBroster.keys()):
						target = 'tab'
						command = command_pairs['-t']
					else:
						target = 'msg'
						command = 'ERROR: switch tab command provided invalid name of tab'
				else:
					target = 'msg'
					command = 'ERROR: switch tab command missing name of tab'

			elif leader == '-p':
				required_pairs = {'-p': None}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					target = 'prune'
				else:
					target = 'msg'
					command = 'ERROR: prune command provided invalid elements'

			elif leader == '-k':
				required_pairs = {'-k': None}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					target = 'kill'
				else:
					target = 'msg'
					command = 'ERROR: kill command provided invalid elements'			
			else:
				target = 'msg'
				command = 'ERROR: no valid flags given'

	if 'target' not in locals():
		target = None
	if 'command' not in locals():
		command = None

	return target, command


## EXECUTABLE ## 
