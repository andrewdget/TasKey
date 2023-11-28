## NOTES ##
'''
1. remember to implement error capturing/handling if function outputs one
2. ComPro currently uses None for Error handling, need to update to something better
'''

## DEPENDENCIES ##
from HeaderFunctions import *
# from UtilityFunctions import *


## DEFINITIONS ##

def ComKey(input_string):
	''' accepts input ("command") string with multiple "markers", composed of a 
	"-" and single letter, followed by an optional string atribute, and outputs 
	a dictionary of marker/attribute pairs ('command_pairs') '''
	markerindex = []
	command_pairs = {}
	nochars = len(input_string)
	for i in range(nochars): # get index of markers
		if input_string[i] == '-':
			markerindex.append(i)
	nomarker = len(markerindex)
	for i in range(nomarker): # get markers and attributes (if they exist)
		marker = input_string[markerindex[i]:markerindex[i]+2]
		if i == nomarker-1: # if last marker/at end of input string
			attribute = input_string[markerindex[i]+3:nochars] # !! Not sure why 'nochars-1' cuts off last char...
		else: # not last marker/at end of input string
			attribute = input_string[markerindex[i]+3:markerindex[i+1]-1]
		if attribute == '':
			attribute = None
		command_pairs.update({marker: attribute})
	return command_pairs


def ComPro(settings, input_string):
	command_pairs = ComKey(input_string)
	if command_pairs != {}:
		function_marker = list(command_pairs.keys())[0]
		
		## DATABASE COMMANDS ##
		if function_marker == '-n':
			new_task = NewTask(settings, command_pairs)
			if new_task != None:
				DB_Manager(add=new_task)
				command = [None, None]
			else:
				command = [None, None]
		elif function_marker == '-e':
			target_index = GetTargetIndex(command_pairs)
			target = DB_Retriever(target_index)
			edited_task = EditTask(target, command_pairs)
			DB_Manager(index=target_index, replacement=edited_task)
			command = [None, None]
		elif function_marker == '-c':
			target_index = GetTargetIndex(command_pairs)
			target = DB_Retriever(target_index)
			completed_task = NewArchivedTask(target, 'completed')
			DB_Manager(index=target_index, complete=completed_task)
			command = [None, None]
		elif function_marker == '-d':
			target_index = GetTargetIndex(command_pairs)
			target = DB_Retriever(target_index)
			deleted_task = NewArchivedTask(target, 'deleted')
			DB_Manager(index=target_index, delete=deleted_task)
			command = [None, None]
		elif function_marker == '-r':
			target_index = GetTargetIndex(command_pairs)
			target = DB_Retriever(target_index, True)
			restored_task = NewRestoredTask(settings, target)
			DB_Manager(index=target_index, restore=restored_task)
			command = [None, None]

		## SCREEN COMMANDS ##
		elif function_marker == '-i':
			command = ['info', command_pairs[function_marker]]
		elif function_marker == '-m':
			command = ['main', None]
		elif function_marker == '-a':
			command = ['archive', None]
		elif function_marker == '-s':
			command = ['settings', command_pairs[function_marker]]

		## OTHER COMMANDS ##
		elif function_marker == '-k':
			command = ['kill', None]
		else:
			command = [False, None]

	else:
		command = [False, None]

	return command

