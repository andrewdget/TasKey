## NOTES ##
'''
1. note TasKey displays dates in diff format than expected Str2Date function 
	date input format... will lead to confusion. Suggest finding fix. 
'''

## DEPENDENCIES ## 

import datetime
from Utils import AlphaIndexer


## DEFINITIONS ##

class TaskDB:
	def __init__(self, config, db_name, path, Active=None, Archive=None):
		self.config = config
		self.db_name = db_name
		self.path = path
		
		if Active == None:
			self.Active = []
		else:
			self.Active = Active

		if Archive == None:
			self.Archive = []
		else:
			self.Archive = Archive


	def new(self, command_pairs):
		priorities = {
			'-c': 'critical',
		 	'-h': 'high',
		 	'-m': 'medium',
		 	'-l': 'low'
		 	}
		flags = list(command_pairs.keys())
		for flag in flags:
			attribute = command_pairs[flag]
			if flag == '-n':
				name = attribute
			elif flag == '-f':
				footnote = attribute
			elif flag in list(priorities.keys()):
				priority = priorities[flag]
			elif flag == '-d':
				deadline = attribute

			if 'footnote' not in locals():
				footnote = None
			if 'priority' not in locals():
				priority = None
			if 'deadline' not in locals():
				deadline = None

		new = ActiveTask(self.config, name, footnote, priority, deadline)
		self.Active.append(new)


	def edit(self, command_pairs):
		priorities = {
			'-c': 'critical',
		 	'-h': 'high',
		 	'-m': 'medium',
		 	'-l': 'low'
		 	}
		flags = list(command_pairs.keys())
		for flag in flags:
			attribute = command_pairs[flag]
			if flag == '-e':
				index = AlphaIndexer(attribute, reverse=True)
			elif flag == '-n':
				self.Active[index].name = attribute
			elif flag == '-f':
				self.Active[index].footnote = attribute
			elif flag in list(priorities.keys()):
				self.Active[index].priority = priorities[flag]
			elif flag == '-d':
				if attribute == None: # allows for elimination of hard deadline
					self.Active[index].deadline = None
					self.Active[index].hard_deadline = False
				else:
					self.Active[index].deadline = attribute
					self.Active[index].hard_deadline = True


	def complete(self, command_pairs):
		index = AlphaIndexer(command_pairs['-c'], reverse=True)
		completed = ArchiveTask(self.config, self.Active[index], 'completed',)
		self.Archive.append(completed)
		del self.Active[index]


	def delete(self, command_pairs):
		index = AlphaIndexer(command_pairs['-d'], reverse=True)
		deleted = ArchiveTask(self.config, self.Active[index], 'deleted',)
		self.Archive.append(deleted)
		del self.Active[index]


	def restore(self, command_pairs):
		index = AlphaIndexer(command_pairs['-r'], reverse=True)
		name = self.Archive[index].name
		footnote = self.Archive[index].footnote
		priority = self.Archive[index].priority
		if self.Archive[index].hard_deadline:
			deadline = self.Archive[index]
		else:
			deadline = None
		restore = ActiveTask(self.config, name, footnote, priority, deadline)
		# restore original auto-generated variables
		restore.created = self.Archive[index].created
		restore.author = self.Archive[index].author
		self.Active.append(restore)
		del self.Archive[index]

	def reindex(self):
		self.Active.sort(key=lambda x: x.created) # done first to insure tasks w/ same score, oldest appear first
		self.Active.sort(key=lambda x: x.score)
		for i in range(len(self.Active)):
			self.Active[i].alpha_index = AlphaIndexer(i)

		self.Archive.sort(key=lambda x: x.occurred, reverse=True)
		for i in range(len(self.Archive)):
			self.Archive[i].alpha_index = AlphaIndexer(i)


class ActiveTask:
	''' DATA VARIABLES
	-Input:
		name
		footnote - additional info/notes for the task
		priority
		deadline

	-From "config":
		author

	-Generated:
		hard_deadline - was the date manualy/automaticaly generated
		created **located above deadline as is requiured for AutoDeadline()**
		remaining - days remaining before deadline
		score - priority score (lower is better)
		alpha_index - double letter (i.e. "aa") index
	'''
	
	def __init__(self, config, name, footnote=None, priority=None, deadline=None):
		self.config = config
		self.name = name
		self.footnote = footnote

		if priority == None:
			self.priority = 'medium'
		else:
			self.priority = priority

		self.created = self.GetCurrentDate()
		if deadline == None:
			self.deadline = self.AutoDeadline()
			self.hard_deadline = False
		else:
			self.deadline = self.Str2Date(deadline)
			self.hard_deadline = True

		self.author = self.config['username']
		self.remaining = self.RegularWorkDayCounter()
		self.score = self.ScorePriority()
		self.alpha_index = None # this will be set later by external routines

		
	def GetCurrentDate(self):
		''' returns current date in datetime format '''
		full_datetime = datetime.datetime.now()
		year = full_datetime.year
		month = full_datetime.month
		day = full_datetime.day
		current_date = datetime.date(year, month, day)
		return current_date


	def Str2Date(self, date):
		''' converts string date (mmddyyyy) into datetime format '''
		if isinstance(date, datetime.date): # confirm date not already in datetime format
			return date
		else:
			year = int(date[4:])
			month = int(date[0:2])
			day = int(date[2:4])
			reformated_date = datetime.date(year, month, day)
			return reformated_date


	def AutoDeadline(self):
		''' generates a deadline for a task based on its priority '''
		if self.priority == 'high':
			deadline = self.created + datetime.timedelta(weeks=self.config['high_period'])
		elif self.priority == 'medium':
			deadline = self.created + datetime.timedelta(weeks=self.config['medium_period'])
		elif self.priority == 'low':
			deadline = self.created + datetime.timedelta(weeks=self.config['low_period'])
		elif self.priority == 'critical':
			deadline = self.created # ritical tasks due the day of creation
		return deadline


	def RegularWorkDayCounter(self):
		''' returns the number of days between current date and deadline, 
		counting only selected regular work days '''
		today = self.GetCurrentDate()
		regular_work_days = [
			self.config['Mon'],
			self.config['Tue'],
			self.config['Wed'],
			self.config['Thu'],
			self.config['Fri'],
			self.config['Sat'],
			self.config['Sun']
			]
		totaldays = (self.deadline - today).days
		count = 0
		for i in range(totaldays + 1):
			tempdate = today + datetime.timedelta(days = i)
			weekday = tempdate.weekday()
			if regular_work_days[weekday] == True:
				count += 1
		return count


	def ScorePriority(self):
		''' returns a "priority score" following a liniar function with a slope
		of 1 and intercept set by priority '''
		if self.priority == 'critical':
			y_intercept = 0
		elif self.priority == 'high':
			y_intercept = 1
		elif self.priority == 'medium':
			y_intercept = 2
		elif self.priority == 'low':
			y_intercept = 3
		priority_score = self.remaining + y_intercept
		return priority_score 


	def refresh(self):
		''' updates deadline (if auto generated), days remaining, and priority
		score. Used when task is edited or restored. '''
		if self.hard_deadline:
			self.deadline = self.Str2Date(self.deadline) # insures deadline in correct format
		else:
			self.deadline = self.AutoDeadline()
		self.remaining = self.RegularWorkDayCounter()
		self.score = self.ScorePriority()


class ArchiveTask:
	''' DATA VARIABLES
	-From "config":
		modifier - who arhived (completed/deleted) the task
	
	-From "task": 
		name
		footnote - additional info/notes for the task
		priority
		deadline
		hard_deadline - was the date manualy/automaticaly generated
		created
		author

	-Input:
		reason - why the task was archived
	
	-Generated:
		occured - when the task was archived
		alpha_index - double letter (i.e. "aa") index
	'''

	def __init__(self, config, task, reason):
		self.modifier = config['username']

		self.name = task.name
		self.footnote = task.footnote
		self.priority = task.priority
		self.deadline = task.deadline
		self.hard_deadline = task.hard_deadline
		self.created = task.created
		self.author = task.author

		self.reason = reason
		
		self.occurred = self.GetCurrentDate()
		self.alpha_index = None # this will be set later by external routines
	

	def GetCurrentDate(self):
		''' returns current date in datetime format '''
		full_datetime = datetime.datetime.now()
		year = full_datetime.year
		month = full_datetime.month
		day = full_datetime.day
		current_date = datetime.date(year, month, day)
		return current_date


## EXECUTABLE ## 
