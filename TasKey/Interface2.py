## NOTES ##
'''
1. ASCII_Datetime function needs to be improved
'''

## DEPENDENCIES ## 

import tkinter as tk
import tkinter.font as tkf
import pyfiglet
import datetime

from FileManagement import *

## DEFINITIONS ##

class TasKeyUI:
	def __init__(self, version, config, DBroster):

		self.DBroster = DBroster

		self.background_color = 'black'
		self.header_color = 'orange'
		self.datetime_color = 'deepskyblue'
		self.progressbar_color = 'slategray3'
		self.progressbar_good_color = 'green'
		self.progressbar_med_color = 'orange'
		self.progressbar_bad_color = 'red'
		self.tab_color = 'white'
		self.tab_bar_color = 'slategray3'
		self.border_color = 'dark olive green'
		self.accent_color = 'seagreen1'
		self.highlight_color = 'red3'
		self.text_color = 'paleturquoise1'
		self.subtext_color = 'darkslategray'
		self.cursor_color = 'red3'
		self.prompt_color = 'red3'





		self.current_win = 'Active'
		self.current_sel = 'aa'
		self.current_tab = list(self.DBroster.keys())[0]
		self.command_msg = False

		self.root = tk.Tk()
		self.root.title('TasKey ' + version)
		self.root.configure(bg=self.background_color)

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
		self.headerwin.config(bg=self.background_color, fg=self.header_color,
			height=6, width=29, borderwidth=0, highlightthickness=0,
			state='disabled')
		self.headerwin.grid(row=0, column=0, rowspan=2, padx=5, sticky='nsew')
		

		self.datetimewin = tk.Text(self.root)
		self.datetimewin.config(bg=self.background_color,
			fg = self.datetime_color, borderwidth=0, height=4, width=70,
			highlightthickness=0,state='disabled')
		self.datetimewin.grid(row=0, column=2, sticky='nsew')

		self.probarwin = tk.Text(self.root)
		self.probarwin.config(bg=self.background_color,
			fg = self.progressbar_color, borderwidth=0, height=2, width=70,
			highlightthickness=0, font='Courier', state='disabled')
		self.probarwin.tag_config('good', foreground=self.progressbar_good_color)
		self.probarwin.tag_config('med', foreground=self.progressbar_med_color)
		self.probarwin.tag_config('bad', foreground=self.progressbar_bad_color)
		self.probarwin.grid(row=1, column=2, sticky='nsew')


		self.tabwin = tk.Text(self.root)
		self.tabwin.config(bg=self.background_color, fg = self.tab_bar_color,
			borderwidth=0, height=3, width=70, highlightthickness=0,
			font='Courier', state='disabled')
		self.tabwin.tag_config('tab', foreground=self.tab_color)
		self.tabwin.tag_config('highlight', foreground=self.highlight_color)
		self.tabwin.grid(row=2, column=0, columnspan=3, padx=5, sticky='nsew')


		self.listframe = tk.Frame(self.root)
		self.listframe.config(borderwidth=0, highlightthickness=2,
			highlightbackground=self.border_color)
		self.listframe.grid(row=3, column=0, columnspan=3, padx=5, sticky='nsew')

		self.listframe.columnconfigure(0, weight=0)
		self.listframe.columnconfigure(1, weight=1)
		self.listframe.columnconfigure(2, weight=0)
		self.listframe.rowconfigure(0, weight=1)

		self.alphaindexwin = tk.Text(self.listframe)
		self.alphaindexwin.config(bg=self.background_color,
			fg=self.accent_color, height=30, width=2, borderwidth=0,
			highlightthickness=0, font='Courier', state='disabled')
		self.alphaindexwin.tag_config('highlight', foreground=self.highlight_color)
		self.alphaindexwin.grid(row=0, column=0, sticky='nsew')

		self.listwin = tk.Text(self.listframe)
		self.listwin.config(bg=self.background_color, fg=self.text_color,
			height=30, width=100, borderwidth=0, highlightthickness=0,
			font='Courier', wrap=tk.WORD, state='disabled')
		self.listwin.grid(row=0, column=1, sticky='nsew')

		self.deadlinewin = tk.Text(self.listframe)
		self.deadlinewin.config(bg=self.background_color, fg=self.subtext_color,
			height=30, width=20, borderwidth=0, highlightthickness=0,
			font='Courier', state='disabled')
		self.deadlinewin.grid(row=0, column=2, sticky='nsew')
		
		self.comwin = tk.Text(self.root)
		self.comwin.config(bg=self.background_color, fg=self.text_color,
			height=3, width=109, borderwidth=0, highlightthickness=2,
			highlightbackground=self.border_color, font='Courier', wrap=tk.WORD,
			insertofftime=300, insertwidth=6,
			insertbackground=self.cursor_color)
		self.comwin.tag_config('prompt', foreground=self.prompt_color)
		self.comwin.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

		self.root.update()
		self.ASCII_Datetime()
		self.ASCII_ProgressBar()
		self.BuildTabs()

		self.root.bind('<Configure>', self.OnResize)


		self.root.mainloop()

	
	def OnResize(self, event):
		self.BuildTabs()
		self.ASCII_ProgressBar()


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

		datetime_str = hour+':'+minute +'  '+ weekday+' ' + month+'. ' +day
		ASCII_datetime = pyfiglet.figlet_format(datetime_str, font='smslant')

		self.datetimewin.config(state='normal')
		self.datetimewin.delete('1.0', tk.END)
		self.datetimewin.insert('1.0', ASCII_datetime)
		self.datetimewin.config(state='disabled')

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

		self.probarwin.config(state='disabled')
		

	def BuildTabs(self):
		self.tabwin.config(state='normal')
		self.tabwin.delete('1.0', tk.END)
		self.tabwin.insert('1.0', '\n\n') # creates required lines
		tabs = list(self.DBroster.keys())
		for tab in tabs:
			nochars = len(tab)
			line1 = ' ' + '_'*nochars + ' '
			line2 = '/' + tab + '\\'
			if tab == self.current_tab:
				self.tabwin.insert('1.end', line1, 'highlight')
				self.tabwin.insert('2.end', line2, 'highlight')
			else:
				self.tabwin.insert('1.end', line1, 'tab')
				self.tabwin.insert('2.end', line2, 'tab')

		[x,y,w,h] = self.root.grid_bbox(0, 2, 2, 2)
		charwidth = tkf.Font(font='Courier').measure('/')
		maxchars = int(w/charwidth - 1)
		tab_len = len(self.tabwin.get('2.0', '2.end'))

		# insures backslashes are at least as long as tabs, even when wrapped
		if tab_len > maxchars:
			self.tabwin.insert('3.0', '\\'*(tab_len + 1))
		else:
			self.tabwin.insert('3.0', '\\'*maxchars)

		self.tabwin.config(state='disabled')

## EXECUTABLE ## 

exec(open('./Data/Paths.txt').read())
exec(open('./Data/Config.txt').read())

DBroster = BatchLoadDB(config, path_roster)

TasKeyUI('v- 0.00.00 (Alpha)', None, DBroster)
