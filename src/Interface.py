## NOTES ##
'''
1. remove executable seciton once done developing
2. implement sytle tags (in general and for command line)
3. develop lengthwise color/tag function
4. need to get resize function working properly w/ applicable widgets
5. keep an eye on clock performance, may need to switch to using multiprocessing
6. set cursor to always on and a thicker marker
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
		hlt = 0 # "1" places box around frames or "naked" text boxes, for debugging

		self.version = version
		self.paths = paths

		# import styles from config
		self.background_color = config['background_color']
		self.header_color = config['header_color']
		self.datetime_color = config['datetime_color']
		self.trim_color = config['trim_color']
		self.text_color = config['text_color']
		self.highlight_color = config['highlight_color']
		self.cursor_color = config['cursor_color']
		self.progress_good_color = config['progress_good_color']
		self.progress_med_color = config['progress_med_color']
		self.progress_bad_color = config['progress_bad_color']
		self.tab_color = config['tab_color']

		# set current state variables
		self.current_win = 'Tasks'
		self.current_tab = list(self.paths.keys())[0]
		self.current_sel = 'aa'

		self.root = tk.Tk()
		self.root.title('TasKey ' + self.version + ' (Beta)')
		self.root.configure(bg=self.background_color)

		# widgets
		self.header = tk.Text(self.root)
		self.header.config(
			bg=self.background_color,
			fg=self.header_color,
			highlightthicknes=hlt,
			height=5,
			width=35
			)

		self.subheader = tk.Text(self.root)
		self.subheader.config(
			bg=self.background_color,
			fg=self.header_color,
			highlightthicknes=hlt,
			font='Courier',
			height=1,
			state='disabled',
			width=0
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
			insertwidth=6,
			insertbackground=self.cursor_color,
			height=3
			)
		self.commandwin.tag_config('highlight', foreground=self.highlight_color)

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
			fg=self.text_color,
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
		self.root.rowconfigure(2, weight=1)
		self.root.rowconfigure(3, weight=1)
		self.root.rowconfigure(4, weight=1)
		self.root.rowconfigure(5, weight=0)

		self.header.grid(row=0, column=0, padx=5, sticky='nsew')
		self.subheader.grid(row=1, column=0, padx=5, sticky='nsew')
		self.listwin.grid(row=2, column=0, rowspan=3, columnspan=2, padx=5, pady=5, sticky='nsew')
		self.infowin.grid(row=4, column=2, padx=5, pady=5, sticky='nsew')
		self.commandwin.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
		self.tabwin.grid(row=0, column=1, rowspan=2, columnspan=2, padx=5, sticky='sew')
		self.datetimewin.grid(row=2, column=2, padx=5, pady=5, sticky='nsew')
		self.progresswin.grid(row=3, column=2, padx=5, pady=5, sticky='nsew')

		# set initial conditions
		self.commandwin.focus_set()
		self.commandwin.insert('1.0', 'TasKey >> ', 'highlight')

		self.ASCII_name = pyfiglet.figlet_format('TasKey', font='smslant')
		self.header.insert('1.0', self.ASCII_name)
		self.header.config(state='disabled')

		self.RefreshTabs()
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
		# self.RefreshTabs()
		pass
		

	def RefreshTabs(self):
			path_names = list(self.paths.keys())
			line1 = ''
			line2 = ''
			for name in path_names:
				nochars = len(name)
				line1 = line1 + ' ' + '_'*nochars + ' '
				line2 = line2 + '/'+name+'\\'
			tabs = line1 + '\n' + line2
			self.tabwin.config(state='normal')
			self.tabwin.delete('1.0', tk.END)
			self.tabwin.insert('1.0', tabs)

			self.root.update()
			[x,y,w,h] = self.root.grid_bbox(1, 0, 2, 1)
			
			charwidth = tkf.Font(font='Courier').measure('/')
			maxchar = int(w/charwidth - 10)

			# insures backslashes are at least as long as tabs, even when wrapped
			if len(line2) > maxchar:
				self.tabwin.insert('3.0', '\n' + '\\'*len(line2))
			else:
				self.tabwin.insert('3.0', '\n' + '\\'*maxchar)
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

		self.root.after(1000, self.ASCII_Datetime)


	def ASCII_ProgressBar(self):
		nochar = 55
		complete = 22
		of = 51
		progress = complete/of
		max_bars = nochar - 9
		no_bars = int(max_bars * progress)
		no_spaces = max_bars - no_bars

		if progress != 1:
			bar ='[' + '/'*no_bars + ' '*no_spaces + '] ' + ' ' + str(round(progress*100, 1)) + '%' + '\n'
		else:
			bar ='[' + '/'*no_bars + ' '*no_spaces + '] ' + str(round(progress*100, 1)) + '%' + '\n'
		
		self.progresswin.config(state='normal')
		self.progresswin.delete('1.0', tk.END)
		self.progresswin.insert('1.0', 'Critical Tasks ' + bar)
		self.progresswin.insert('2.0', '   Total Tasks ' + bar)
		self.progresswin.insert('3.0', '  Weekly Tasks ' + bar)
		self.progresswin.config(state='disabled')


## EXECUTABLE ## 

version = 'v- 00.05.06'

paths = {
   'Main': '/some/junk/goes/here',
   'S1': '/some/junk/goes/here',
   'Bubs<3': '/some/junk/goes/here',
   'Dogs': '/some/junk/goes/here',
   'Long Test': '/some/junk/goes/here',
   'Anotha One': '/some/junk/went/here'
}

config = {
	'background_color': 'black',
	'header_color': 'orange',
	'datetime_color': 'turquoise1',
	'trim_color': 'grey40',
	'text_color': 'white',
	'highlight_color': 'red',
	'cursor_color': 'white',
	'progress_good_color': 'green',
	'progress_med_color': 'orange',
	'progress_bad_color': 'red',
	'tab_color': 'white'
	}

TasKeyUI(version, config,  paths)

