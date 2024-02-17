## NOTES ##
'''

'''

## DEPENDENCIES ## 

import datetime
from Utils import AlphaIndexer, GetCurrentDate, Str2Date


## DEFINITIONS ##

class TaskDB:
	def __init__(self, config, db_name, Active=None, Archive=None):
		self.config = config
		self.db_name = db_name
		
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
				assert attribute != None
				name = attribute
			elif flag == '-f':
				assert attribute != None
				footnote = attribute
			elif flag in list(priorities.keys()):
				priority = priorities[flag]
			elif flag == '-d':
				assert attribute != None
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
			'-c': 'Critical',
		 	'-h': 'High',
		 	'-m': 'Medium',
		 	'-l': 'Low'
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
					self.Active[index].deadline = Str2Date(attribute)
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


	def hard_delete(self, command_pairs):
		index = AlphaIndexer(command_pairs['-d'], reverse=True)
		del self.Archive[index]


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


	def refresh(self):
		for i in range(len(self.Active)):
			self.Active[i].refresh()


	def reindex(self):
		self.Active.sort(key=lambda x: x.created)
		self.Active.sort(key=lambda x: x.score)
		for i in range(len(self.Active)):
			self.Active[i].alpha_index = AlphaIndexer(i)

		self.Archive.sort(key=lambda x: x.occurred, reverse=True)
		for i in range(len(self.Archive)):
			self.Archive[i].alpha_index = AlphaIndexer(i)


	def stats(self):
		noworkdays = 0
		for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
			if self.config[day]:
				noworkdays += 1
		threshold = GetCurrentDate() + datetime.timedelta(days=noworkdays)
		
		stats = {'total': 0, 'total_complete': 0, 'critical': 0,
			'critical_complete': 0}
		for task in self.Active:
			if task.deadline <= threshold:
				stats['total'] += 1
				if task.priority == 'Critical':
					stats['critical'] += 1
		for task in self.Archive:
			if task.deadline <= threshold:
				if task.reason == 'completed':
					stats['total'] += 1
					stats['total_complete'] += 1
					if task.priority == 'Critical':
						stats['critical'] += 1
						stats['critical_complete'] += 1
		return stats


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
		hard_deadline - was the date manually/automatically generated
		created **located above deadline as is required for AutoDeadline()**
		remaining - days remaining before deadline
		score - priority score (lower is better)
		alpha_index - double letter (i.e. "aa") index
	'''
	
	def __init__(self, config, name, footnote=None, priority=None, deadline=None):
		self.config = config
		self.name = name
		self.footnote = footnote

		if priority == None:
			self.priority = 'Medium'
		else:
			self.priority = priority

		self.created = GetCurrentDate()
		if deadline == None:
			self.deadline = self.AutoDeadline()
			self.hard_deadline = False
		else:
			self.deadline = Str2Date(deadline)
			self.hard_deadline = True

		self.author = self.config['username']
		self.remaining = self.RegularWorkDayCounter()
		self.score = self.ScorePriority()
		self.alpha_index = None # this will be set later by external routines


	def AutoDeadline(self):
		''' generates a deadline for a task based on its priority '''
		if self.priority == 'High':
			deadline = self.created + datetime.timedelta(weeks=self.config['high_period'])
		elif self.priority == 'Medium':
			deadline = self.created + datetime.timedelta(weeks=self.config['medium_period'])
		elif self.priority == 'Low':
			deadline = self.created + datetime.timedelta(weeks=self.config['low_period'])
		elif self.priority == 'Critical':
			deadline = self.created # critical tasks due the day of creation
		return deadline


	def RegularWorkDayCounter(self):
		''' returns the number of days between current date and deadline, 
		counting only selected regular work days '''
		today = GetCurrentDate()
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
		''' returns a "priority score" following a linear function with a slope
		of 1 and intercept set by priority '''
		if self.priority == 'Critical':
			y_intercept = 0
		elif self.priority == 'High':
			y_intercept = 1
		elif self.priority == 'Medium':
			y_intercept = 2
		elif self.priority == 'Low':
			y_intercept = 3
		priority_score = self.remaining + y_intercept
		return priority_score 


	def refresh(self):
		''' updates deadline (if auto generated), days remaining, and priority
		score. Used when task is edited or restored. '''
		if self.hard_deadline:
			self.deadline = Str2Date(self.deadline) # insures deadline in correct format
		else:
			self.deadline = self.AutoDeadline()
		self.remaining = self.RegularWorkDayCounter()
		self.score = self.ScorePriority()


class ArchiveTask:
	''' DATA VARIABLES
	-From "config":
		modifier - who archived (completed/deleted) the task
	
	-From "task": 
		name
		footnote - additional info/notes for the task
		priority
		deadline
		hard_deadline - was the date manually/automatically generated
		created
		author

	-Input:
		reason - why the task was archived
	
	-Generated:
		occurred - when the task was archived
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
		
		self.occurred = GetCurrentDate()
		self.alpha_index = None # this will be set later by external routines


## EXECUTABLE ## 
