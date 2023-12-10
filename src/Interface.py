## NOTES ##
'''
1. progress bar values are currently hard coded
2. monitor clock performance, may need to switch to using multiprocessing
'''

## DEPENDENCIES ## 

import tkinter as tk
import tkinter.font as tkf
import pyfiglet
import datetime

## DEFINITIONS ##

class TasKeyUI:
	def __init__(self, version, config, paths):

		# development setting
		hlt = 0 # '1' places box around naked frames/text boxes for dev purposes

		self.version = version
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

		# set current state variables
		self.current_win = 'Tasks'
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
			highlightthicknes=hlt,
			padx=10,
			height=5,
			width=30
			)

		self.listwin = tk.Text(self.root)
		self.listwin.config(
			bg=self.background_color,
			fg=self.text_color,
			highlightbackground=self.trim_color,
			highlightthicknes=2,
			state='disabled'
			)

		self.infowin = tk.Text(self.root)
		self.infowin.config(
			bg=self.background_color,
			fg=self.text_color,
			highlightbackground=self.trim_color,
			highlightthicknes=2,
			state='disabled'
			)

		self.commandwin = tk.Text(self.root)
		self.commandwin.config(
			bg=self.background_color,
			fg=self.text_color,
			highlightcolor=self.trim_color,
			highlightbackground=self.trim_color,
			highlightthicknes=2,
			font='Courier',
			insertofftime=300,
			padx=5,
			insertwidth=6,
			insertbackground=self.cursor_color,
			height=3
			)
		self.commandwin.tag_config('highlight', foreground=self.prompt_color)

		self.tabwin = tk.Text(self.root)
		self.tabwin.config(
			bg=self.background_color,
			fg=self.tab_color,
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
			highlightthicknes=hlt,
			state='disabled',
			padx=5,
			height=5,
			)

		self.progresswin = tk.Text(self.root)
		self.progresswin.config(
			bg=self.background_color,
			fg=self.progressbar_color,
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
		self.commandwin.insert('1.0', 'TasKey >> ', 'highlight')

		self.ASCII_name = pyfiglet.figlet_format('TasKey', font='smslant')
		self.header.insert('1.0', self.ASCII_name)
		self.header.config(state='disabled')

		self.root.update()
		self.PathTabs()
		self.ASCII_Datetime()
		self.ASCII_ProgressBar()


		# bindings
		self.root.bind('<Configure>', self.OnResize)
		self.commandwin.bind('<FocusOut>', self.FocusReturn)
		self.commandwin.bind('<KeyRelease>', self.PromptProtect)

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
				self.commandwin.insert('1.0', 'TasKey >> ', 'highlight')


	def OnResize(self, event):
		self.PathTabs()
		self.ASCII_ProgressBar()
		

	def PathTabs(self):
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

		weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
		weekday = weekdays[current.weekday()]
		day = str(current.day)
		month = str(current.month)
		year = str(current.year)

		datetime_str = hour+':'+minute +' '+ weekday+' ' + month+'.' +day
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


## EXECUTABLE ## 

# version = 'v- 00.05.06'

# paths = {
#    'Main': '/some/junk/goes/here',
#    'S1': '/some/junk/goes/here',
#    'Bubs<3': '/some/junk/goes/here',
#    'Dogs': '/some/junk/goes/here',
#    'Long Test': '/some/junk/goes/here',
#    'Anotha One': '/some/junk/went/here'
# }

# config = {
# 	'background_color': 'black',
# 	'header_color': 'orange',
# 	'prompt_color': 'mediumpurple2',
# 	'datetime_color': 'deepskyblue',
# 	'trim_color': 'darkslategray',
# 	'text_color': 'paleturquoise1',
# 	'highlight_color': 'mediumpurple2',
# 	'cursor_color': 'paleturquoise1',
# 	'progressbar_color': 'slategray3',
# 	'progress_good_color': 'green',
# 	'progress_med_color': 'orange',
# 	'progress_bad_color': 'red',
# 	'tab_color': 'slategray3',
# 	'tab_bar_color': 'slategray3'
# 	}

# TasKeyUI(version, config,  paths)
