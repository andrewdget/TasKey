## NOTES ##
'''

'''

## DEPENDENCIES ## 
import datetime


## DEFINITIONS ##

def ComInt(input_string):
	''' accepts an input string with multiple "flags" (i.e. "-a", "-b", etc.)
	followed by an optional string attribute and outputs a dictionary of
	flag/attribute pairs ('command_pairs') '''
	flagindex = []
	command_pairs = {}
	nochars = len(input_string)
	for i in range(nochars): # get index of flags
		if input_string[i] == '-':
			if i == 0 or input_string[i-1] == ' ':
				flagindex.append(i)
	noflag = len(flagindex)
	for i in range(noflag): # get flags and attributes (if they exist)
		flag = input_string[flagindex[i]:flagindex[i]+2]
		if i == noflag-1: # if last flag/at end of input string
			attribute = input_string[flagindex[i]+3:nochars]
		else:
			attribute = input_string[flagindex[i]+3:flagindex[i+1]-1]
		if attribute == '':
			attribute = None
		command_pairs.update({flag: attribute})
	return command_pairs


def ComValidation(command_pairs, required_pairs):
	''' validates output of ComKey() function, verifying that it contains the
	required pairs for downstream functions, see 'required_pairs' format example
	below:

	required_pairs = {
		'-a': 'req', 		# single flag w/ attribute required
		'-b': 'opt',		# single flag w/ attribute optional
		'-c': None,			# single flag w/ no attribute allowed
		'-d/-e': 'req',		# multi-choice flag w/ attribute required
		'-f/-g': 'opt',		# multi-choice flag w/ attribute optional
		'-h/-i': None		# multi-choice flag w/ no attribute allowed
	'''

	command_flags = set(list(command_pairs.keys()))
	required_flags = set(list(required_pairs.keys()))
	valid = True 
	for flag in required_flags:
		if '/' in flag:
			options = set(flag.split('/'))
			match = options.intersection(command_flags)
			if match: 
				match = list(match)[0]
				if required_pairs[flag] == 'req':
					if command_pairs[match] == None:
						valid = False
				elif required_pairs[flag] == None:
					if command_pairs[match] != None:
						valid = False
			else:
				valid = False
		else:
			if flag in command_flags:
				match = flag
				if required_pairs[match] == 'req':
					if command_pairs[match] == None:
						valid = False
				elif required_pairs[match] == None:
					if command_pairs[match] != None:
						valid = False
			else:
				valid = False
	return valid


def ComPro(DBroster, current_tab, current_win, input_str):
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
						command = 'ERROR: new task command contains invalid'\
							' elements'
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
						command = 'ERROR: edit task command contains invalid'\
							' elements'
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
						command = 'ERROR: complete task command contains an'\
							' invalid index'
				else:
					target = 'msg'
					command = 'ERROR: complete task command missing index'

			elif leader == '-d':
				required_pairs = {'-d': 'req'}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					try:
						if current_win == 'Archive':
							DB.hard_delete(command_pairs)
						else:
							DB.delete(command_pairs)
					except:
						target = 'msg'
						command = 'ERROR: delete task command contains an'\
						' invalid index'
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
						command = 'ERROR: restore task command contains an'\
						' invalid index'
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
						command = 'ERROR: information command contains an'\
							' invalid index'
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
					command = 'ERROR: switch to main command provided invalid'\
						' elements'

			elif leader == '-a':
				required_pairs = {'-a': None}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					target = 'win'
					command = 'Archive'
				else:
					target = 'msg'
					command = 'ERROR: switch to archive command provided'\
						' invalid elements'	

			elif leader == '-t':
				required_pairs = {'-t': 'req'}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					if command_pairs['-t'] in list(DBroster.keys()):
						target = 'tab'
						command = command_pairs['-t']
					else:
						target = 'msg'
						command = 'ERROR: switch tab command provided invalid'\
							' name of tab'
				else:
					target = 'msg'
					command = 'ERROR: switch tab command missing name of tab'

			elif leader == '-s':
				required_pairs = {'-s': None}
				validation = ComValidation(command_pairs, required_pairs)
				if validation:
					target = 'save'
				else:
					target = 'msg'
					command = 'ERROR: save command provided invalid elements'

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


def AlphaIndexer(input_index, reverse=False):
	''' 
	if reverse=False (default):
		function returns a double character, alphabetical, index given a
		numerical equivalent i.e. 1 = aa, 27 = ba, etc. 
	if reverse=True:
		function returns a numerical index given a double character,
		alphabetical, index i.e. aa = 1, ba = 27, etc.
	'''
	ABC = 'abcdefghijklmnopqrstuvwxyz'
	if reverse == False:
		# ".01" insures char1 increases after 26, rather than at 26
		char1 = int((input_index+1)/26.01)
		char2 = ((input_index+1) % 26) - 1
		output_index = ABC[char1] + ABC[char2]
	elif reverse == True:
		char1 = input_index[0]
		char2 = input_index[1]
		for i in range(26):
			if ABC[i] == char1:
				index1 = i * 26
			if ABC[i] == char2:
				index2 = i
		output_index = index1 + index2
	return output_index


def GetCurrentDate():
	''' returns current date in datetime format '''
	full_datetime = datetime.datetime.now()
	year = full_datetime.year
	month = full_datetime.month
	day = full_datetime.day
	current_date = datetime.date(year, month, day)
	return current_date


def Str2Date(date):
	''' converts string date (mmddyyyy) into datetime format '''
	if isinstance(date, datetime.date): # confirm not already in datetime format
		return date
	else:
		year = int(date[4:])
		month = int(date[0:2])
		day = int(date[2:4])
		reformated_date = datetime.date(year, month, day)
		return reformated_date


## EXECUTABLE ## 
