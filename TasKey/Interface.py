## NOTES ##
'''

'''

## DEPENDENCIES ## 

import tkinter as tk
import tkinter.font as tkf
import pyfiglet
import datetime
import math

from CommandProcessor import *
from FileManagement import BatchPrune

## DEFINITIONS ##

class TasKeyUI:
	def __init__(self, version, config, DBroster):

		self.config = config
		self.DBroster = DBroster


		background_color = self.config['background_color']
		header_color = self.config['header_color']
		datetime_color = self.config['datetime_color']
		progressbar_color = self.config['progressbar_color']
		progressbar_good_color = self.config['progressbar_good_color']
		progressbar_med_color = self.config['progressbar_med_color']
		progressbar_bad_color = self.config['progressbar_bad_color']
		tab_color = self.config['tab_color']
		border_color = self.config['border_color']
		accent_color = self.config['accent_color']
		highlight_color = self.config['highlight_color']
		text_color = self.config['text_color']
		subtext_color = self.config['subtext_color']
		cursor_color = self.config['cursor_color']
		prompt_color = self.config['prompt_color']
		view_status_color = self.config['view_status_color']


		# UI state variables
		self.current_win = 'Active'
		self.current_sel = None
		self.current_tab = list(self.DBroster.keys())[0]
		self.command_msg = False


		self.root = tk.Tk()
		self.root.title('TasKey ' + version)
		self.root.configure(bg=background_color)

		self.root.columnconfigure(0, weight=0)
		self.root.columnconfigure(1, weight=1)
		self.root.columnconfigure(2, weight=0)
		self.root.rowconfigure(0, weight=0)
		self.root.rowconfigure(1, weight=0)
		self.root.rowconfigure(2, weight=0)
		self.root.rowconfigure(3, weight=1)
		self.root.rowconfigure(4, weight=0)


		self.headerwin = tk.Text(self.root)
		self.headerwin.insert('1.0', '\n' + pyfiglet.figlet_format('TasKey',
			font = 'smslant'))
		self.headerwin.delete('7.0', tk.END)
		self.headerwin.config(bg=background_color, fg=header_color,
			height=6, width=29, borderwidth=0, highlightthickness=0,
			state='disabled')
		self.headerwin.grid(row=0, column=0, rowspan=2, padx=10, sticky='nsew')
		

		self.datetimeframe = tk.Frame(self.root)
		self.datetimeframe.config(
			borderwidth=0, highlightthickness=0)
		self.datetimeframe.grid(row=0, column=2, sticky='nsew')

		self.datetimeframe.columnconfigure(0, weight=0)
		self.datetimeframe.columnconfigure(1, weight=0)
		self.datetimeframe.columnconfigure(2, weight=0)
		self.datetimeframe.rowconfigure(0, weight=0)


		self.timewin = tk.Text(self.datetimeframe)
		self.timewin.config(bg=background_color, fg=datetime_color,
			borderwidth=0, height=4, width=25, highlightthickness=0,
			state='disabled')
		self.timewin.tag_config('center', justify=tk.CENTER)
		self.timewin.grid(row=0, column=0, sticky='nsew')
		

		self.weekdaywin = tk.Text(self.datetimeframe)
		self.weekdaywin.config(bg=background_color, fg=datetime_color,
			borderwidth=0, height=4, width=20, highlightthickness=0,
			state='disabled')
		self.weekdaywin.tag_config('center', justify=tk.CENTER)
		self.weekdaywin.grid(row=0, column=1, sticky='nsew')


		self.datewin = tk.Text(self.datetimeframe)
		self.datewin.config(bg=background_color, fg=datetime_color,
			borderwidth=0, height=4, width=25, highlightthickness=0,
			state='disabled')
		self.datewin.tag_config('center', justify=tk.CENTER)
		self.datewin.grid(row=0, column=2, sticky='nsew')


		self.probarwin = tk.Text(self.root)
		self.probarwin.config(bg=background_color,
			fg = progressbar_color, borderwidth=0, height=2, width=0,
			highlightthickness=0, font='Courier', state='disabled')
		self.probarwin.tag_config('good', foreground=progressbar_good_color)
		self.probarwin.tag_config('med', foreground=progressbar_med_color)
		self.probarwin.tag_config('bad', foreground=progressbar_bad_color)
		self.probarwin.grid(row=1, column=2, sticky='nsew')


		self.tabwin = tk.Text(self.root)
		self.tabwin.config(bg=background_color, fg = tab_color,
			borderwidth=0, height=2, width=0, highlightthickness=0,
			font='Courier', state='disabled')
		self.tabwin.tag_config('highlight', foreground=highlight_color)
		self.tabwin.grid(row=2, column=0, columnspan=3, padx=5, sticky='nsew')


		self.listwin = tk.Text(self.root)
		self.listwin.config(bg=background_color, fg=text_color,	height=30, 
			width=120, borderwidth=0, highlightthickness=1,
			highlightbackground=border_color, font='Courier', wrap=tk.WORD,
			state='disabled')
		self.listwin.tag_config('status', foreground=view_status_color)
		self.listwin.tag_config('accent', foreground=accent_color)
		self.listwin.tag_config('subtext', foreground=subtext_color)
		self.listwin.tag_config('highlight', foreground=highlight_color)
		self.listwin.grid(row=3, column=0, columnspan=3, padx=5, sticky='nsew')


		self.comwin = tk.Text(self.root)
		self.comwin.config(bg=background_color, fg=text_color,
			height=3, width=0, borderwidth=0, highlightthickness=1,
			highlightbackground=border_color, highlightcolor=border_color,
			font='Courier', wrap=tk.WORD, insertofftime=300, insertwidth=6,
			insertbackground=cursor_color)
		self.comwin.tag_config('prompt', foreground=prompt_color)
		self.comwin.grid(row=4, column=0, columnspan=3, padx=5, pady=5,
			sticky='nsew')


		self.root.update()
		self.ASCII_Datetime()
		self.ASCII_ProgressBar()
		self.BuildTabs()
		self.FocusReturn()
		self.PromptProtect()
		self.DispRefresh()


		self.root.bind('<Configure>', self.OnResize)
		self.comwin.bind('<FocusOut>', self.FocusReturn)
		self.comwin.bind('<KeyRelease>', self.PromptProtect)
		self.comwin.bind('<Return>', self.CommandReturn)


		self.root.mainloop()


	def ASCII_Datetime(self):
		ct = datetime.datetime.now()
		hour = '{0:02.0f}'.format(ct.hour)
		minute = '{0:02.0f}'.format(ct.minute)
		weekdays = ['Mon', 'Tus', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
		weekday = weekdays[ct.weekday()]
		day = '{0:02.0f}'.format(ct.day)
		month = '{0:02.0f}'.format(ct.month)

		self.timewin.config(state='normal')
		self.timewin.delete('1.0', tk.END)
		ASCII_time = pyfiglet.figlet_format(hour + ':' + minute, font='smslant')
		self.timewin.insert('1.0', ASCII_time, 'center')
		self.timewin.delete('5.0', tk.END)
		self.timewin.config(state='disabled')
		
		self.weekdaywin.config(state='normal')
		self.weekdaywin.delete('1.0', tk.END)
		ASCII_weekday = pyfiglet.figlet_format(weekday, font='smslant')
		self.weekdaywin.insert('1.0', ASCII_weekday, 'center')
		self.weekdaywin.delete('5.0', tk.END)
		self.weekdaywin.config(state='disabled')

		self.datewin.config(state='normal')
		self.datewin.delete('1.0', tk.END)
		ASCII_date = pyfiglet.figlet_format(month + '. ' + day, font='smslant')
		self.datewin.insert('1.0', ASCII_date, 'center')
		self.datewin.delete('5.0', tk.END)
		self.datewin.config(state='disabled')

		self.root.after(1000, self.ASCII_Datetime)


	def ASCII_ProgressBar(self):

		def BarColor(complete, of, barchar_length, bad, med):
			precent = complete/of
			no_bars = int(barchar_length * precent)
			no_space = barchar_length - no_bars

			rel_bad = int(barchar_length*bad)
			rel_med = int(barchar_length*med)

			bar = '/'*no_bars + '-'*no_space
			for i in range(len(bar)):
				char = bar[i]
				if char == '/':
					if i < rel_bad:
						self.probarwin.insert(tk.END, char, 'bad')
					elif i < rel_med:
						self.probarwin.insert(tk.END, char, 'med')
					else:
						self.probarwin.insert(tk.END, char, 'good')
				else:
					self.probarwin.insert(tk.END, char)

		[x,y,w,h] = self.root.grid_bbox(2, 1)
		packaging_length = tkf.Font(font='Courier').measure('Critical Tasks [] 000.0%')
		charwidth = tkf.Font(font='Courier').measure('/')
		barchar_length = int((w - packaging_length)/charwidth - 1)

		self.probarwin.config(state='normal')
		self.probarwin.delete('1.0', tk.END)

		critical = 5
		critical_complete = 1
		critical_precent = str(round((critical_complete/critical)*100, 1))
		self.probarwin.insert('1.0', 'Critical Tasks [')
		BarColor(critical_complete, critical, barchar_length, 0.5, 0.75)
		self.probarwin.insert(tk.END, '] ' + critical_precent + '%' + '\n')

		weekly = 10
		weekly_complete = 5
		weekly_precent = str(round((weekly_complete/weekly)*100, 1))
		self.probarwin.insert('2.0', '  Weekly Tasks [')
		BarColor(weekly_complete, weekly, barchar_length, 0.25, 0.5)
		self.probarwin.insert(tk.END, '] ' + weekly_precent + '%' + '\n')

		self.probarwin.delete('3.0', tk.END)
		self.probarwin.config(state='disabled')
		

	def BuildTabs(self):
		self.tabwin.config(state='normal')
		self.tabwin.delete('1.0', tk.END)
		self.tabwin.insert('1.0', '\n\n')
		tabs = list(self.DBroster.keys())
		for tab in tabs:
			line1 = ' ' + '_'*len(tab) + ' '
			line2 = '/' + tab + '\\'
			if tab == self.current_tab:
				self.tabwin.insert('1.end', line1, 'highlight')
				self.tabwin.insert('2.end', line2, 'highlight')
			else:
				self.tabwin.insert('1.end', line1)
				self.tabwin.insert('2.end', line2)
		self.tabwin.delete('3.0', tk.END)
		self.tabwin.config(state='disabled')


	def FocusReturn(self,event=None):
		self.comwin.focus_set()


	def PromptProtect(self, event=None):
		cursor_position = self.comwin.index(tk.INSERT)
		[cursor_line, cursor_column] = cursor_position.split('.')
		if int(cursor_line) == 1:
			if int(cursor_column) < 10:
				self.comwin.delete('1.0', '1.10')
				self.comwin.insert('1.0', 'TasKey >> ', 'prompt')


	def DispRefresh(self):
		self.BuildTabs()
		self.DBroster[self.current_tab].refresh()
		self.DBroster[self.current_tab].reindex()

		self.listwin.config(state='normal')
		self.listwin.delete('1.0', tk.END)

		[x,y,w,h] = self.root.grid_bbox(0, 3, 2, 3)
		charwidth = tkf.Font(font='Courier').measure('0')
		buffer = tkf.Font(font='Courier').measure('  aa  //0000-00-00 [000]')
		wraplen = int((w-buffer)/charwidth)
		if self.current_win == 'Active':
			self.listwin.insert('1.0', '//Main//\n', 'status')
			for task in self.DBroster[self.current_tab].Active:
				if task.alpha_index != self.current_sel:
					config = {
						'L1': '  ' + task.alpha_index + '  ',
						'L2': '      ',
						'F1': ' //' + str(task.deadline) + ' [' +\
							'{0:03.0f}'.format(task.remaining) + ']',
						'L1tag': 'accent',
						'F1tag': 'subtext',
						'tag': None,
						'wrap': wraplen,
						'width': w,
						'charwidth': charwidth
						}
					self.AddBranch(task.name, config)
					if task.footnote != None:
						config = {
							'L1': u'      \u2514\u2500\u2500 ',
							'L2': '          ',
							'F1': None,
							'L1tag': 'subtext',
							'F1tag': None,
							'tag': 'subtext',
							'wrap': wraplen,
							'width': w,
							'charwidth': charwidth
							}
						self.AddBranch(task.footnote, config)
				else:
					config = {
						'L1': '  ' + task.alpha_index + '  ',
						'L2': '      ',
						'F1': ' //' + str(task.deadline) + ' [' +\
							'{0:03.0f}'.format(task.remaining) + ']',
						'L1tag': 'highlight',
						'F1tag': 'subtext',
						'tag': 'accent',
						'wrap': wraplen,
						'width': w,
						'charwidth': charwidth
						}
					self.AddBranch(task.name, config)
					config = {
							'L1': u'      \u251c\u2500\u2500 ',
							'L2': u'      \u2502   ',
							'F1': None,
							'L1tag': 'subtext',
							'F1tag': None,
							'tag': 'subtext',
							'wrap': wraplen,
							'width': w,
							'charwidth': charwidth
							}
					self.AddBranch('Footnote: ' + str(task.footnote), config)
					self.listwin.insert(tk.END, u'      \u2502\n', 'subtext')
					config = {
						'L1': u'      \u251c\u2500\u2500 ',
						'L2': '          ',
						'F1': None,
						'L1tag': 'subtext',
						'F1tag': None,
						'tag': 'subtext',
						'wrap': wraplen,
						'width': w,
						'charwidth': charwidth
						}
					self.AddBranch('Priority.........' + task.priority, config)
					self.AddBranch('Priority Score...' +\
						str(task.score), config)
					if not task.hard_deadline:
						self.AddBranch('Deadline.........' +\
							str(task.deadline) + '(Auto)', config)
					else:
						self.AddBranch('Deadline.........' +\
							str(task.deadline) + '(Manual)', config)
					self.AddBranch('Days Remaining...' +\
						str(task.remaining), config)
					self.AddBranch('Created By.......' + task.author, config)
					config = {
						'L1': u'      \u2514\u2500\u2500 ',
						'L2': '          ',
						'F1': None,
						'L1tag': 'subtext',
						'F1tag': None,
						'tag': 'subtext',
						'wrap': wraplen,
						'width': w,
						'charwidth': charwidth
						}
					self.AddBranch('Created on.......' +\
						str(task.created), config)
		else:
			self.listwin.insert('1.0', '!!ARCHIVE!!\n', 'highlight')
			for task in self.DBroster[self.current_tab].Archive:
				if task.alpha_index != self.current_sel:
					config = {
						'L1': '  ' + task.alpha_index + '  ',
						'L2': '      ',
						'F1': ' //' + str(task.occurred),
						'L1tag': 'accent',
						'F1tag': 'subtext',
						'tag': None,
						'wrap': wraplen,
						'width': w,
						'charwidth': charwidth
						}
					self.AddBranch(task.name, config)
					if task.footnote != None:
						config = {
							'L1': u'      \u2514\u2500\u2500 ',
							'L2': '          ',
							'F1': None,
							'L1tag': 'subtext',
							'F1tag': None,
							'tag': 'subtext',
							'wrap': wraplen,
							'width': w,
							'charwidth': charwidth
							}
						self.AddBranch(task.footnote, config)
				else:
					config = {
						'L1': '  ' + task.alpha_index + '  ',
						'L2': '      ',
						'F1': ' //' + str(task.occurred),
						'L1tag': 'highlight',
						'F1tag': 'subtext',
						'tag': 'accent',
						'wrap': wraplen,
						'width': w,
						'charwidth': charwidth
						}
					self.AddBranch(task.name, config)
					config = {
							'L1': u'      \u251c\u2500\u2500 ',
							'L2': u'      \u2502   ',
							'F1': None,
							'L1tag': 'subtext',
							'F1tag': None,
							'tag': 'subtext',
							'wrap': wraplen,
							'width': w,
							'charwidth': charwidth
							}
					self.AddBranch('Footnote: ' + task.footnote, config)
					self.listwin.insert(tk.END, u'      \u2502\n', 'subtext')
					config = {
						'L1': u'      \u251c\u2500\u2500 ',
						'L2': '          ',
						'F1': None,
						'L1tag': 'subtext',
						'F1tag': None,
						'tag': 'subtext',
						'wrap': wraplen,
						'width': w,
						'charwidth': charwidth
						}
					self.AddBranch('Priority.........' + task.priority, config)
					if not task.hard_deadline:
						self.AddBranch('Deadline.........' +\
							str(task.deadline) + '(Auto)', config)
					else:
						self.AddBranch('Deadline.........' +\
							str(task.deadline) + '(Manual)', config)
					self.AddBranch('Created By.......' + task.author, config)
					self.AddBranch('Created on.......' +\
						str(task.created), config)
					self.AddBranch('Modified By......' +\
						task.modifier, config)
					self.AddBranch('Modified on......' +\
						str(task.occurred), config)
					config = {
						'L1': u'      \u2514\u2500\u2500 ',
						'L2': '          ',
						'F1': None,
						'L1tag': 'subtext',
						'F1tag': None,
						'tag': 'subtext',
						'wrap': wraplen,
						'width': w,
						'charwidth': charwidth
						}
					self.AddBranch('Reason..........' + task.reason, config)
		self.listwin.config(state='disabled')


	def AddBranch(self, string, config):
		''' TKinter's build in text wrapping functionality was insufficient when
		trying to implement TasKey's task display scheme (based on unicode file
		trees). This function allows for dynamic wrapping and inclusion of tree
		elements.
		'''
		# u'\u251c' # T-symbol
		# u'\u2514' # L-symbol
		# u'\u2502' # vertical line
		# u'\u2500' # horizontal line

		L1 = config['L1'] # first line "Leader" string
		L2 = config['L2'] # "Leader" string for subsequent lines
		F1 = config['F1'] # first line "Follower" string
		L1tag = config['L1tag'] # first line "Leader" tag
		F1tag = config['F1tag'] # first line "Follower" tag
		tag = config['tag'] # general body tag
		wrap = config['wrap'] # wrap length in characters
		width = config['width'] # width of listwin in pixels
		charwidth = config['charwidth'] # character width in pixels

		branch = {0: ''}
		total = 0
		currentline = 0
		for word in string.split(' '):
			wordlen = len(word)
			if total + wordlen != len(string):
				addition = word + ' '
				total += len(addition)
			else:
				addition = word
			linelen = len(branch[currentline]) + len(addition)
			if linelen <= wrap:
				if branch[currentline] != '':
					branch[currentline] += addition
				else:
					branch[currentline] = L1 + addition
			else:
				currentline += 1
				try:
					branch[currentline] += addition
				except:
					branch[currentline] = L2 + addition

		for key in list(branch.keys()):
			if key > 0:
				self.listwin.insert(tk.END, branch[key] + '\n', tag)
			else:
				self.listwin.insert(tk.END, branch[key][:len(L1)], L1tag)
				self.listwin.insert(tk.END, branch[key][len(L1):], tag)
				if F1 != None:
					remaining = int(width/charwidth - len(branch[key]) - 2)
					buffer = ' ' * (remaining - len(F1))
					self.listwin.insert(tk.END, buffer + F1 + '\n', F1tag)
				else:
					self.listwin.insert(tk.END, '\n')


	def OnResize(self, event):
		self.BuildTabs()
		self.ASCII_ProgressBar()
		self.DispRefresh()


	def CommandReturn(self, event):
		if self.command_msg == False:
			com_input = self.comwin.get('1.10', tk.END).strip()
			[target, command] = ComPro(self.DBroster[self.current_tab],
				com_input)
			self.comwin.delete('1.10', tk.END)
			self.UICommandProcessor(target, command)
		else:
			self.comwin.config(state='normal')
			self.comwin.delete('1.0', tk.END)
			self.comwin.insert('1.0', 'TasKey >> ', 'prompt') 
			self.command_msg = False
		return 'break'


	def UICommandProcessor(self, target, command):
		if target != None:
			if target == 'sel':
				self.current_sel = command
			elif target == 'win':
				self.current_win = command
				self.current_sel == None
			elif target == 'tab':
				self.current_tab = command
			elif target == 'msg':
				self.CommandMsg(command)
			elif target == 'prune':
				path_roster = {}
				for name in list(self.DBroster.keys()):
					path_roster[name] = self.DBroster[name].path
				BatchPrune(path_roster, del_all=False)
			elif target == 'kill':
				self.root.destroy()				
				return self.DBroster
		self.DispRefresh()


	def CommandMsg(self, message):
		self.command_msg = True
		self.commandwin.delete('1.0', tk.END)
		self.commandwin.insert('1.0', message, 'highlight')
		self.commandwin.insert(tk.END, ' <press enter to continue>', 'prompt')
		self.commandwin.config(state='disabled')
