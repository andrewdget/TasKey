## NOTES ##
'''
1. progress bar values are currently hard coded
2. monitor clock performance, may need to switch to using multiprocessing
3. condiser making portions of config file that pertain to theme/style seperate
	to support creation of default/custom themes as well as sharing.
4. add headers to indicate what is being shown in listwin
'''

## DEPENDENCIES ## 

import tkinter as tk
import tkinter.font as tkf
import pyfiglet
import datetime

from CommandProcessor import *

## DEFINITIONS ##

class TasKeyUI:
	def __init__(self, version, config, temp_db, paths):

		# development setting
		hlt = 0 # '1' places box around naked frames/text boxes for dev purposes

		self.version = version
		self.CurrentDB = temp_db
		self.paths = paths

		# import styles from config
		self.background_color = config['background_color']
		self.header_color = config['header_color']
		self.prompt_color = config['prompt_color']
		self.datetime_color = config['datetime_color']
		self.trim_color = config['trim_color']
		self.text_color = config['text_color']
		self.highlight_color = config['highlight_color']
		self.cursor_color = config['cursor_color']
		self.progressbar_color = config['progressbar_color']
		self.progress_good_color = config['progress_good_color']
		self.progress_med_color = config['progress_med_color']
		self.progress_bad_color = config['progress_bad_color']
		self.tab_color = config['tab_color']
		self.tab_bar_color = config['tab_bar_color']
		self.accent_color = config['accent_color']

		# set current state variables
		self.current_win = 'Archive'
		self.current_tab = list(self.paths.keys())[0]
		self.current_sel = 'aa'

		self.root = tk.Tk()
		self.root.title('TasKey ' + self.version)
		self.root.configure(bg=self.background_color)

		# widgets
		self.header = tk.Text(self.root)
		self.header.config(
			bg=self.background_color,
			fg=self.header_color,
			borderwidth=0,
			highlightthicknes=hlt,
			padx=10,
			height=5,
			width=30
			)


		self.listwin = tk.Text(self.root)
		self.listwin.config(
			bg=self.background_color,
			fg=self.text_color,
			borderwidth=0,
			width=60,
			highlightbackground=self.trim_color,
			highlightthicknes=1,
			state='disabled'
			)
		self.listwin.tag_config('index', foreground=self.accent_color)
		self.listwin.tag_config('highlight', foreground=self.highlight_color)


		self.infowin = tk.Text(self.root)
		self.infowin.config(
			bg=self.background_color,
			fg=self.text_color,
			borderwidth=0,
			width=0,
			highlightbackground=self.trim_color,
			highlightthicknes=1,
			state='disabled'
			)
		self.infowin.tag_config('header', foreground=self.accent_color)
		self.infowin.tag_config('highlight', foreground=self.highlight_color)


		self.commandwin = tk.Text(self.root)
		self.commandwin.config(
			bg=self.background_color,
			fg=self.text_color,
			borderwidth=0,
			width=0,
			highlightcolor=self.trim_color,
			highlightbackground=self.trim_color,
			highlightthicknes=1,
			font='Courier',
			insertofftime=300,
			padx=5,
			insertwidth=6,
			insertbackground=self.cursor_color,
			height=3
			)
		self.commandwin.tag_config('prompt', foreground=self.prompt_color)


		self.tabwin = tk.Text(self.root)
		self.tabwin.config(
			bg=self.background_color,
			fg=self.tab_color,
			borderwidth=0,
			width=0,
			highlightthicknes=hlt,
			font='Courier',
			wrap=tk.NONE,
			state='disabled',
			height=3,
			)
		self.tabwin.tag_config('bar', foreground=self.tab_bar_color)
		self.tabwin.tag_config('highlight', foreground=self.highlight_color)


		self.datetimewin = tk.Text(self.root)
		self.datetimewin.config(
			bg=self.background_color,
			fg=self.datetime_color,
			borderwidth=0,
			width=0,
			highlightthicknes=hlt,
			state='disabled',
			padx=5,
			height=5,
			)


		self.progresswin = tk.Text(self.root)
		self.progresswin.config(
			bg=self.background_color,
			fg=self.progressbar_color,
			borderwidth=0,
			width=0,
			highlightthicknes=hlt,
			font='Courier',
			state='disabled',
			padx=5,
			pady=5,
			height=3,
			)
		self.progresswin.tag_config('good', foreground=self.progress_good_color)
		self.progresswin.tag_config('med', foreground=self.progress_med_color)	
		self.progresswin.tag_config('bad', foreground=self.progress_bad_color)


		self.root.columnconfigure(0, weight=0)
		self.root.columnconfigure(1, weight=1)
		self.root.columnconfigure(2, weight=1)

		self.root.rowconfigure(0, weight=0)
		self.root.rowconfigure(1, weight=0)
		self.root.rowconfigure(2, weight=0)
		self.root.rowconfigure(3, weight=1)
		self.root.rowconfigure(4, weight=0)

		self.header.grid(row=0, column=0, padx=5, sticky='nsew')
		self.listwin.grid(row=1, column=0, rowspan=3, columnspan=2, padx=5, pady=5, sticky='nsew')
		self.infowin.grid(row=3, column=2, padx=5, pady=5, sticky='nsew')
		self.commandwin.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
		self.tabwin.grid(row=0, column=1, columnspan=2, padx=5, sticky='sew')
		self.datetimewin.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')
		self.progresswin.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')


		# set initial conditions
		self.commandwin.focus_set()
		self.commandwin.insert('1.0', 'TasKey >> ', 'prompt')

		self.ASCII_name = pyfiglet.figlet_format('TasKey', font='smslant')
		self.header.insert('1.0', self.ASCII_name)
		self.header.config(state='disabled')

		self.root.update()
		self.BuildTabs()
		self.ASCII_Datetime()
		self.ASCII_ProgressBar()


		# bindings
		self.root.bind('<Configure>', self.OnResize)
		self.commandwin.bind('<FocusOut>', self.FocusReturn)
		self.commandwin.bind('<KeyRelease>', self.PromptProtect)
		self.commandwin.bind('<Return>', self.CommandReturn)

		self.root.mainloop()


	# definitions 
	def FocusReturn(self,event):
		self.commandwin.focus_set()


	def PromptProtect(self, event):
		cursor_position = self.commandwin.index(tk.INSERT)
		[cursor_line, cursor_column] = cursor_position.split('.')
		if int(cursor_line) == 1:
			if int(cursor_column) < 10:
				self.commandwin.delete('1.0', '1.10')
				self.commandwin.insert('1.0', 'TasKey >> ', 'prompt')

	def CommandReturn(self, event):
		input_raw = self.commandwin.get('1.10', tk.END) # includes the erroneus '\n' at end
		input_stripped = input_raw[0:len(input_raw)-1] # ending '\n' stripped
		command = ComPro(self.CurrentDB, input_stripped)
		self.commandwin.delete('1.10', tk.END)
		self.DispRefresh()
		return 'break'

	def OnResize(self, event):
		self.BuildTabs()
		self.ASCII_ProgressBar()
		

	def BuildTabs(self):
		self.tabwin.config(state='normal')
		self.tabwin.delete('1.0', tk.END)
		self.tabwin.insert('1.0', '\n\n') # creates required lines
		path_names = list(self.paths.keys())
		for name in path_names:
			nochars = len(name)
			line1 = ' ' + '_'*nochars + ' '
			line2 = '/' + name + '\\'
			if name == self.current_tab:
				self.tabwin.insert('1.end', line1, 'highlight')
				self.tabwin.insert('2.end', line2, 'highlight')
			else:
				self.tabwin.insert('1.end', line1)
				self.tabwin.insert('2.end', line2)

		[x,y,w,h] = self.root.grid_bbox(1, 0, 2, 0)
		charwidth = tkf.Font(font='Courier').measure('/')
		maxchars = int(w/charwidth - 3)
		tab_len = len(self.tabwin.get('2.0', '2.end'))

		# insures backslashes are at least as long as tabs, even when wrapped
		if tab_len > maxchars:
			self.tabwin.insert('3.0', '\\'*(tab_len + 1), 'bar')
		else:
			self.tabwin.insert('3.0', '\\'*maxchars, 'bar')

		self.tabwin.config(state='disabled')


	def ASCII_Datetime(self):
		current = datetime.datetime.now()

		hour = str(current.hour)
		if len(hour) == 1:
			hour = '0' + hour
		minute = str(current.minute)
		if len(minute) == 1:
			minute = '0' + minute

		weekdays = ['Mon', 'Tus', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
		weekday = weekdays[current.weekday()]
		day = str(current.day)
		month = str(current.month)
		year = str(current.year)

		datetime_str = hour+':'+minute +'  '+ weekday+' ' + month+'.' +day
		ASCII_datetime = pyfiglet.figlet_format(datetime_str, font='smslant')

		self.datetimewin.config(state='normal')
		self.datetimewin.delete('1.0', tk.END)
		self.datetimewin.insert('1.0', ASCII_datetime)
		self.datetimewin.config(state='disabled')

		layer = ASCII_datetime.split('\n')[0]
		width = tkf.Font(font='Courier').measure(layer)
		self.root.columnconfigure(2, minsize=width)

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
						self.progresswin.insert(tk.END, char, 'bad')
					elif i < rel_med:
						self.progresswin.insert(tk.END, char, 'med')
					else:
						self.progresswin.insert(tk.END, char, 'good')
				else:
					self.progresswin.insert(tk.END, char)

		[x,y,w,h] = self.root.grid_bbox(2, 2)
		packaging_length = tkf.Font(font='Courier').measure('Critical Tasks [] 000.0%')
		charwidth = tkf.Font(font='Courier').measure('/')
		barchar_length = int((w - packaging_length)/charwidth - 3)

		self.progresswin.config(state='normal')
		self.progresswin.delete('1.0', tk.END)

		critical = 5
		critical_complete = 1
		critical_precent = str(round((critical_complete/critical)*100, 1))
		self.progresswin.insert('1.0', 'Critical Tasks [')
		BarColor(critical_complete, critical, barchar_length, 0.5, 0.75)
		self.progresswin.insert(tk.END, '] ' + critical_precent + '%' + '\n')

		weekly = 10
		weekly_complete = 5
		weekly_precent = str(round((weekly_complete/weekly)*100, 1))
		self.progresswin.insert('2.0', '  Weekly Tasks [')
		BarColor(weekly_complete, weekly, barchar_length, 0.25, 0.5)
		self.progresswin.insert(tk.END, '] ' + weekly_precent + '%' + '\n')

		total = 28
		total_complete  = 8
		total_precent = str(round((total_complete/total)*100, 1))
		self.progresswin.insert('3.0', '   Total Tasks [')
		BarColor(total_complete, total, barchar_length, 0.1, 0.25)
		self.progresswin.insert(tk.END, '] ' + total_precent + '%')

		self.progresswin.config(state='disabled')


	def DispRefresh(self):
		# self.current_win = 'Active'
		# self.current_sel = 'aa'
		self.BuildTabs()
		self.CurrentDB.reindex()

		self.listwin.config(state='normal')
		self.listwin.delete('1.0', tk.END)
		self.infowin.config(state='normal')
		self.infowin.delete('1.0', tk.END)

		if self.current_win == 'Active':
			for task in self.CurrentDB.Active:
				alpha_index = task.alpha_index
				if alpha_index == self.current_sel:
					self.listwin.insert(tk.END, alpha_index, 'highlight')
					self.listwin.insert(tk.END, ' ' + task.name + '\n')

					self.infowin.insert(tk.END, 'Task Name: ', 'header')
					self.infowin.insert(tk.END, task.name + '\n')
					self.infowin.insert(tk.END, 'Footnote: ', 'header')
					self.infowin.insert(tk.END, str(task.footnote) + '\n')
					self.infowin.insert(tk.END, 'Priority: ', 'header')
					self.infowin.insert(tk.END, task.priority + '\n')
					self.infowin.insert(tk.END, 'Score: ', 'header')
					self.infowin.insert(tk.END, str(task.score) + '\n')

					self.infowin.insert(tk.END, 'Deadline: ', 'header')
					if task.hard_deadline:
						self.infowin.insert(tk.END, str(task.deadline))
						self.infowin.insert(tk.END, ' (Manual)\n', 'highlight')
					else:
						self.infowin.insert(tk.END, str(task.deadline))
						self.infowin.insert(tk.END, ' (Auto)\n', 'highlight')

					self.infowin.insert(tk.END, 'Working Days Remaining: ', 'header')
					self.infowin.insert(tk.END, str(task.remaining) + '\n')
					self.infowin.insert(tk.END, 'Created by: ', 'header')
					self.infowin.insert(tk.END, task.author + '\n')
					self.infowin.insert(tk.END, 'Created on: ', 'header')
					self.infowin.insert(tk.END, str(task.created) + '\n')

				else:
					self.listwin.insert(tk.END, alpha_index, 'index')
					self.listwin.insert(tk.END, ' ' + task.name + '\n')
		elif self.current_win == 'Archive':
			for task in self.CurrentDB.Archive:
				alpha_index = task.alpha_index
				if alpha_index == self.current_sel:
					self.listwin.insert(tk.END, alpha_index, 'highlight')
					self.listwin.insert(tk.END, ' ' + task.name + '\n')

					self.infowin.insert(tk.END, 'Task Name: ', 'header')
					self.infowin.insert(tk.END, task.name + '\n')
					self.infowin.insert(tk.END, 'Footnote: ', 'header')
					self.infowin.insert(tk.END, str(task.footnote) + '\n')
					self.infowin.insert(tk.END, 'Priority: ', 'header')
					self.infowin.insert(tk.END, task.priority + '\n')
					
					self.infowin.insert(tk.END, 'Deadline: ', 'header')
					if task.hard_deadline:
						self.infowin.insert(tk.END, str(task.deadline))
						self.infowin.insert(tk.END, ' (Manual)\n', 'highlight')
					else:
						self.infowin.insert(tk.END, str(task.deadline))
						self.infowin.insert(tk.END, ' (Auto)\n', 'highlight')

					self.infowin.insert(tk.END, 'Created by: ', 'header')
					self.infowin.insert(tk.END, task.author + '\n')
					self.infowin.insert(tk.END, 'Created on: ', 'header')
					self.infowin.insert(tk.END, str(task.created) + '\n')
					self.infowin.insert(tk.END, 'Modified by: ', 'header')
					self.infowin.insert(tk.END, task.modifier + '\n')
					self.infowin.insert(tk.END, 'Modified on: ', 'header')
					self.infowin.insert(tk.END, str(task.occurred) + '\n')
					self.infowin.insert(tk.END, 'Reason: ', 'header')
					self.infowin.insert(tk.END, task.reason + '\n')


				else:
					self.listwin.insert(tk.END, alpha_index, 'index')
					self.listwin.insert(tk.END, ' ' + task.name + '\n')



		self.listwin.config(state='disabled')
		self.infowin.config(state='disabled')






