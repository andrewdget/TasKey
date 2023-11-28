## NOTES ##
'''

'''


## DEPENDENCIES ##

from CommandFunctions import *


## CONSTANTS ## 

settings = {
	'Mon': True,
	'Tue': True,
	'Wed': True,
	'Thu': True,
	'Fri': True,
	'Sat': False,
	'Sun': False,
	'HPeriod': 1,
	'MPeriod': 2,
	'LPeriod': 3
	}


## DEFINITIONS ##

def DispMain(TaskDB):
	print('------------Main------------')
	for i in range(len(TaskDB)):
		print(TaskDB[i].alpha_index + '-\t' + TaskDB[i].name)
	print()
	print('////////////End////////////')
	print()

def DispArchive(ArchiveDB):
	print('------------Archive------------')
	for i in range(len(ArchiveDB)):
		print(ArchiveDB[i].alpha_index + '-\t' + ArchiveDB[i].name)
	print()
	print('////////////End////////////')
	print()

def DispInfo(alpha_index, in_archive=False):
	index = AlphaIndexer(alpha_index, reverse=True)
	target = DB_Retriever(index, in_archive)

	if in_archive:
		print('Name: ' + target.name)
		print('Priority: ' + target.priority)
		if target.hard_deadline:
			print('Deadline: ' + str(target.deadline) + ' (Hard)')
		else:
			print('Deadline: ' + str(target.deadline) + ' (Auto Generated)')
		print('Occurred: ' + str(target.occurred))
		print('Reason: ' + target.reason)
		print('Footnote: ' + str(target.footnote))

	else:
		print('------------Info------------')
		print('Name: ' + target.name)
		print('Priority: ' + target.priority)
		if target.hard_deadline:
			print('Deadline: ' + str(target.deadline) + ' (Hard)')
		else:
			print('Deadline: ' + str(target.deadline) + ' (Auto Generated)')
		print('Created: ' + str(target.created))
		print('Days Remaining: ' + str(target.remaining))
		print('Priority Score: ' + str(target.score))
		print('Footnote: ' + str(target.footnote)) # use 'str()' for case where footnote=None
		print()
		print('////////////End////////////')
		print()


## WORKINGSPACE ## 

initial_inputs = [
	'nonesense -n Follow up with Cole -l -f Need more info about the FR',
	'-n Complete Nov Saw Training -m',
	'-n Finish Coding DB manager def -c',
	'-n This one must be done -d 12142023 -h',
	'-n Come up with addtional tasks -h',
	'-n Figure out how to manage global vars -m -f w/ multiple modules',
	'-n Think about how this will all integrate with UI -l'
	]

working_inputs = [
	'-e ae -c',
	'-c ab',
	'-d ad',
	'-r aa',
	'-i aa'
	]

for i in range(len(initial_inputs)):
	ComPro(settings, initial_inputs[i])

command = ComPro(settings, working_inputs[4])
print(command)

print(TaskDB[0].name)
# DispMain(TaskDB)

# ComPro(settings, working_inputs[0])
# ComPro(settings, working_inputs[1])
# ComPro(settings, working_inputs[2])
# ComPro(settings, working_inputs[3])

# DispMain(TaskDB)
# DispArchive(ArchiveDB)

# DsipInfo('aa', True)














