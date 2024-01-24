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
			flagindex.append(i)
	noflag = len(flagindex)
	for i in range(noflag): # get flags and attributes (if they exist)
		flag = input_string[flagindex[i]:flagindex[i]+2]
		if i == noflag-1: # if last flag/at end of input string
			attribute = input_string[flagindex[i]+3:nochars] # !! Not sure why 'nochars-1' cuts off last char...
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
			match = options.intersection(command_flags) # checks if any of the options are in command_flags list
			if match: # this is all that is required for 'opt' attributes
				match = list(match)[0] # convert back from set() data structure
				if required_pairs[flag] == 'req': # use 'flag' here as 'match' is delimited component of the 'required_pairs' dict
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
		char1 = int((input_index+1)/26.01) # .01 insures char1 increases after 26, rather than at 26
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
	if isinstance(date, datetime.date): # confirm date not already in datetime format
		return date
	else:
		year = int(date[4:])
		month = int(date[0:2])
		day = int(date[2:4])
		reformated_date = datetime.date(year, month, day)
		return reformated_date

## EXECUTABLE ## 
