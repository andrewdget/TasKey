## NOTES ##
'''
1. need to modify SpecialDayCounter to count backwards if required
2. need to add methods for DB local save/load (and checking if var exists)
	- Maybe create seperate module for database location and other settings info
3. Priority score method for tasks with a hard deadline creates an undesirably
	high (low) priority score because remaining days is potentialy high.
'''


## DEPENDENCIES ##

import datetime
from UtilityFunctions import *
from FileFunctions import *

## CLASSES ##

class Task:
	def __init__(self, settings, name, priority, deadline=None, footnote=None, alpha_index=None):
		self.settings = settings
		self.name = name
		self.priority = priority
		self.footnote = footnote
		self.alpha_index = alpha_index

		self.created = self.GetCurrentDate()

		if deadline != None: # if deadline is set manualy
			self.deadline = self.Str2Date(deadline)
			self.hard_deadline = True # prevents autodeadlineing when editing task
		else:
			self.deadline = self.AutoDeadline()
			self.hard_deadline = False

		self.remaining = self.SpecialDayCounter()
		self.score = self.ScorePriority()

	def GetCurrentDate(self):
		''' returns current date in datetime format '''
		rawdate = datetime.datetime.now()
		year = rawdate.year
		month = rawdate.month
		day = rawdate.day
		currentdate = datetime.date(year, month, day)
		return currentdate

	def Str2Date(self, date):
		''' converts string date (mmddyyyy) into datetime format '''
		year = int(date[4:])
		month = int(date[0:2])
		day = int(date[2:4])
		reformdate = datetime.date(year, month, day)
		return reformdate

	def AutoDeadline(self):
		''' generates a deadline for a task based on its priority '''
		if self.priority == 'high':
			deadline = self.created + datetime.timedelta(weeks=self.settings['HPeriod'])
		elif self.priority == 'medium':
			deadline = self.created + datetime.timedelta(weeks=self.settings['MPeriod'])
		elif self.priority == 'low':
			deadline = self.created + datetime.timedelta(weeks=self.settings['LPeriod'])
		elif self.priority == 'critical':
			deadline = self.created # ritical tasks due the day of creation
		return deadline

	def SpecialDayCounter(self):
		''' returns the number of days between current date and deadline, 
		counting only selected weekdays '''
		today = self.GetCurrentDate()
		special_days = [
			self.settings['Mon'],
			self.settings['Tue'],
			self.settings['Wed'],
			self.settings['Thu'],
			self.settings['Fri'],
			self.settings['Sat'],
			self.settings['Sun']
			]
		totaldays = (self.deadline - today).days
		count = 0
		for i in range(totaldays + 1):
			tempdate = today + datetime.timedelta(days = i)
			weekday = tempdate.weekday()
			if special_days[weekday] == True:
				count += 1
		return count

	def ScorePriority(self):
		''' returns a "Priority Score" follwoing a liniar function with a slope
		of 1 and intercept set by priority '''
		if self.priority == 'critical':
			y_intercept = 0
		elif self.priority == 'high':
			y_intercept = 1
		elif self.priority == 'medium':
			y_intercept = 2
		elif self.priority == 'low':
			y_intercept = 3
		priorityscore = self.remaining + y_intercept # Y = (M)(X) + B
		return priorityscore 

	def refresh(self):
		''' updates deadline (if autogenerated), days remaining, and priority
		score. Used when task is edited. '''
		if self.hard_deadline:
			self.deadline = self.Str2Date(self.deadline) # insures deadline in correct format	
		else:
			self.deadline = self.AutoDeadline()
		self.remaining = self.SpecialDayCounter()
		self.score = self.ScorePriority()


class ArchivedTask:
	def __init__(self, name, priority, created, deadline, hard_deadline, reason, footnote=None, alpha_index=None):
		self.name = name	
		self.priority = priority
		self.created = created
		self.deadline = deadline
		self.hard_deadline = hard_deadline
		self.reason = reason
		self.footnote = footnote

		self.occurred = self.GetCurrentDate()

	def GetCurrentDate(self):
		''' returns current date in datetime format '''
		rawdate = datetime.datetime.now()
		year = rawdate.year
		month = rawdate.month
		day = rawdate.day
		currentdate = datetime.date(year, month, day)
		return currentdate

## DEFINITIONS ##

def DB_Manager(add=None, index=None, replacement=None, complete=None, delete=None, restore=None):
	global TaskDB, ArchiveDB
	if add != None: # new task
		TaskDB.append(add)
		TaskDB.sort(key=lambda x: x.created) # done first to insure tasks w/ same score, oldest appear first
		TaskDB.sort(key=lambda x: x.score)
		for i in range(len(TaskDB)):
			TaskDB[i].alpha_index = AlphaIndexer(i)
	elif replacement != None: # edit task
		TaskDB[index] = replacement
		TaskDB.sort(key=lambda x: x.created) # done first to insure tasks w/ same score, oldest appear first
		TaskDB.sort(key=lambda x: x.score)
		for i in range(len(TaskDB)):
			TaskDB[i].alpha_index = AlphaIndexer(i)
	elif complete != None: # complete task
		del TaskDB[index]
		for i in range(len(TaskDB)):
			TaskDB[i].alpha_index = AlphaIndexer(i)
		ArchiveDB.append(complete)
		ArchiveDB.sort(key=lambda x: x.occurred, reverse=True)
		for i in range(len(ArchiveDB)):
			ArchiveDB[i].alpha_index = AlphaIndexer(i)
	elif delete != None: # delete task
		del TaskDB[index]
		for i in range(len(TaskDB)):
			TaskDB[i].alpha_index = AlphaIndexer(i)
		ArchiveDB.append(delete)
		ArchiveDB.sort(key=lambda x: x.occurred, reverse=True)
		for i in range(len(ArchiveDB)):
			ArchiveDB[i].alpha_index = AlphaIndexer(i)
	elif restore != None: # restor task
		del ArchiveDB[index]
		for i in range(len(ArchiveDB)):
			ArchiveDB[i].alpha_index = AlphaIndexer(i)
		TaskDB.append(restore)
		TaskDB.sort(key=lambda x: x.created) # done first to insure tasks w/ same score, oldest appear first
		TaskDB.sort(key=lambda x: x.score)
		for i in range(len(TaskDB)):
			TaskDB[i].alpha_index = AlphaIndexer(i)


def DB_Size(check_archive=False):
	if check_archive:
		size = len(ArchiveDB)
	else:
		size = len(TaskDB)
	return size


def DB_Retriever(index, in_archive=False):
	if in_archive:
		item = ArchiveDB[index]
	else:
		item = TaskDB[index]
	return item

[TaskDB, ArchiveDB] = SafeLoadDB()
