## NOTES ##
'''
1. need to add method for deleting hard deadlines and removing footnotes
2. need to add validation to each header function, functions should return
	'None' if validation fails.
'''

## DEPENDENCIES ##
from DatabaseFunctions import *
from UtilityFunctions import *

## DEFINITIONS ##

def NewTask(settings, command_pairs):
	required_pairs = {'-n': 'attribute', '-c/-h/-m/-l': None}
	valid = ComValidation(command_pairs, required_pairs)
	if valid:	
		priorities = {'-c': 'critical', '-h': 'high', '-m': 'medium', '-l': 'low'}
		markers = list(command_pairs.keys())
		for marker in markers:
			attribute = command_pairs[marker]
			if marker == '-n':
				name = attribute
			elif marker == '-d':
				deadline = attribute
			elif marker == '-f':
				footnote = attribute
			elif marker in list(priorities.keys()):
				priority = priorities[marker]
		if 'deadline' not in locals():
			deadline = None
		if 'footnote' not in locals():
			footnote = None
		new_task = Task(settings, name, priority, deadline, footnote)
	else:
		new_task = None
	return new_task


def EditTask(old_task, command_pairs):
	markers = list(command_pairs.keys())
	if len(markers) > 1:
		edited_task = old_task
		priorities = {'-c': 'critical', '-h': 'high', '-m': 'medium', '-l': 'low'}
		for marker in markers:
			attribute = command_pairs[marker]
			if marker == '-n':
				edited_task.name = attribute
			elif marker == '-d':
				edited_task.deadline = attribute
				edited_task.hard_deadline = True
			elif marker == '-f':
				edited_task.footnote = attribute
			elif marker in list(priorities.keys()):
				edited_task.priority = priorities[marker]
		edited_task.refresh()
		return edited_task
	else:
		edited_task = None
		return edited_task


def NewArchivedTask(task, reason):
	name = task.name
	priority = task.priority
	created = task.created
	deadline = task.deadline
	hard_deadline = task.hard_deadline
	footnote = task.footnote
	archived_task = ArchivedTask(name, priority, created, deadline, hard_deadline, reason, footnote)
	return archived_task


def NewRestoredTask(settings, archived_task):
	name = archived_task.name
	priority = archived_task.priority
	created = archived_task.created
	footnote = archived_task.footnote
	if archived_task.hard_deadline == True:
		deadline = archived_task.deadline
	else:
		deadline = None
	restored_task = Task(settings, name, priority, deadline, footnote)
	restored_task.created = created
	restored_task.refresh()
	return restored_task











