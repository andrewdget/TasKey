## NOTES ##
'''
1. need to modify ComValidation to accept multiple spaces after marker
'''

## DEPENDENCIES ##


## DEFINITIONS ##

def ComValidation(command_pairs, required_pairs):
	''' validates output of ComKey() function against 'required_pairs' dict to
	verify that it contains the required pairs for downstream functions. See
	format below:

	required_pairs = {
		'-a': 'attribute', 		# single marker w/ attribute required
		'-b': None,				# single marker w/ out required attribute
		'-c/-d': 'attribute',	# multi-choice marker w/ attribute required
		'-e/-f': None			# multi-choice marker w/ out required attribute
		}
	'''
	command_markers = set(list(command_pairs.keys()))
	required_markers = set(list(required_pairs.keys()))
	valid = True 
	for marker in required_markers:
		if '/' in marker: # indicates multiple choice, required marker
			options = set(marker.split('/'))
			match = options.intersection(command_markers) # checks if any of the options are in command_markers list
			if match:
				match = list(match)[0] # convert back from set() data structure
				if required_pairs[marker] == 'attribute': # use 'marker' here as 'match' is dilimited component of the 'required_pairs' dict
					if command_pairs[match] == None:
						valid = False
				elif required_pairs[marker] == None:
					if command_pairs[match] != None:
						valid = False
			else:
				valid = False
		else:
			if marker in command_markers:
				match = marker
				if required_pairs[match] == 'attribute':
					if command_pairs[match] == None:
						valid = False
				elif required_pairs[match] == None:
					if command_pairs[match] != None:
						valid = False
			else:
				valid = False
	return valid


def AlphaIndexer(input_index, reverse=False):
	''' if reverse=False (default):
			function returns a double character, alphabetical, index given a
			numerical equivilant i.e. 1 = aa, 27 = ba, etc. 
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


def GetTargetIndex(command_pairs):
	marker = list(command_pairs.keys())[0]
	alpha_index = command_pairs[marker]
	target_index = AlphaIndexer(alpha_index, reverse=True)
	return target_index
