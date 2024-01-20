## NOTES ##
'''
1. Consider improving the ASCII_ProgressBar funciton
'''

## DEPENDENCIES ## 

import tkinter as tk
import tkinter.font as tkf
import pyfiglet
import datetime
import time

from FileManagement import *

## DEFINITIONS ##

class TasKeyUI:
	def __init__(self, version, config, DBroster):

		self.DBroster = DBroster


		# unpack color settings
		background_color = 'black'
		header_color = 'orange'
		datetime_color = 'deepskyblue'
		progressbar_color = 'slategray3'
		progressbar_good_color = 'green'
		progressbar_med_color = 'orange'
		progressbar_bad_color = 'red'
		tab_color = 'slategray3'
		border_color = 'darkslategray'
		accent_color = 'seagreen1'
		highlight_color = 'red3'
		text_color = 'paleturquoise1'
		subtext_color = 'darkslategray'
		cursor_color = 'red3'
		prompt_color = 'red3'


		# UI state variables
		self.current_win = 'Active'
		self.current_sel = 'aa'
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
			borderwidth=0, height=2, width=70, highlightthickness=0,
			font='Courier', state='disabled')
		self.tabwin.tag_config('highlight', foreground=highlight_color)
		self.tabwin.grid(row=2, column=0, columnspan=3, padx=5, sticky='nsew')


		self.listframe = tk.Frame(self.root)
		self.listframe.config(borderwidth=0, highlightthickness=1,
			highlightbackground=border_color)
		self.listframe.grid(row=3, column=0, columnspan=3, padx=5, sticky='nsew')

		self.listframe.columnconfigure(0, weight=0)
		self.listframe.columnconfigure(1, weight=1)
		self.listframe.columnconfigure(2, weight=0)
		self.listframe.rowconfigure(0, weight=1)


		self.alphaindexwin = tk.Text(self.listframe)
		self.alphaindexwin.config(bg=background_color,
			fg=accent_color, height=30, width=2, borderwidth=0,
			highlightthickness=0, font='Courier', state='disabled')
		self.alphaindexwin.tag_config('highlight', foreground=highlight_color)
		self.alphaindexwin.grid(row=0, column=0, sticky='nsew')


		self.listwin = tk.Text(self.listframe)
		self.listwin.config(bg=background_color, fg=text_color,
			height=30, width=100, borderwidth=0, highlightthickness=0,
			font='Courier', wrap=tk.WORD, state='disabled')
		self.listwin.grid(row=0, column=1, sticky='nsew')


		self.deadlinewin = tk.Text(self.listframe)
		self.deadlinewin.config(bg=background_color, fg=subtext_color,
			height=30, width=20, borderwidth=0, highlightthickness=0,
			font='Courier', state='disabled')
		self.deadlinewin.grid(row=0, column=2, sticky='nsew')
		

		self.comwin = tk.Text(self.root)
		self.comwin.config(bg=background_color, fg=text_color,
			height=3, width=109, borderwidth=0, highlightthickness=1,
			highlightbackground=border_color, highlightcolor=border_color,
			font='Courier', wrap=tk.WORD, insertofftime=300, insertwidth=6,
			insertbackground=cursor_color)
		self.comwin.tag_config('prompt', foreground=prompt_color)
		self.comwin.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')


		self.root.update()
		self.ASCII_Datetime()
		self.ASCII_ProgressBar()
		self.BuildTabs()
		self.FocusReturn()
		self.PromptProtect()


		self.root.bind('<Configure>', self.OnResize)
		self.comwin.bind('<FocusOut>', self.FocusReturn)
		self.comwin.bind('<KeyRelease>', self.PromptProtect)

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


	def OnResize(self, event):
		self.BuildTabs()
		self.ASCII_ProgressBar()


## EXECUTABLE ## 

exec(open('./Data/Paths.txt').read())
exec(open('./Data/Config.txt').read())

DBroster = BatchLoadDB(config, path_roster)

TasKeyUI('v- 0.00.00 (Alpha)', None, DBroster)




