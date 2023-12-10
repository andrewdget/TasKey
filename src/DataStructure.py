## NOTES ##
'''
1. note TasKey displays dates in diff format than expected Str2Date function 
	date input format... will lead to confusion. Suggest finding fix. 
'''

## DEPENDENCIES ## 

import datetime


## DEFINITIONS ##

class TaskDB:
	def __init__(self, db_name, path):
		self.db_name = db_name
		self.path = path # ?? is this needed ??
		
		self.Active = []
		self.Archive = []


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
		created
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

		if deadline == None:
			self.deadline = AutoDeadline()
			self.hard_deadline = False
		else:
			self.deadline = self.Str2Date(deadline)
			self.hard_deadline = True

		self.author = self.config['username']
		self.created = self.GetCurrentDate()
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
			deadline = self.created + datetime.timedelta(weeks=self.config['medium_eriod'])
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
		score. Used when task is edited. '''
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

	def __init__(self, config, task, reason, modifier):
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
