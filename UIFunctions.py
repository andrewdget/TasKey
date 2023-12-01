## NOTES ##
'''
1. Need to add save functionality to kill command

'''

## DEPENDENCIES ##
import tkinter as tk
from CommandFunctions import *

## DEFINITIONS ##

class TasKeyUI:
	def __init__(self, parent, settings):
		self.parent = parent
		self.settings = settings

		self.current_win = 'main'
		self.current_sel = 'aa'

		frame_color = 'turquoise1'

		self.parent.title('TasKey')
		self.parent.configure(width=1200, height=600, bg='black')
		self.parent.minsize(600, 500)

		self.listframe = tk.Frame(self.parent, bg='black', padx=8, pady=8, highlightthicknes=0)
		self.listframe.place(x=0, y=0, relwidth=0.70, relheight=0.90)
		self.listwin = tk.Text(self.listframe, state='disabled', bg='black', fg='white', highlightbackground=frame_color, highlightthicknes=2)
		self.listwin.pack(expand=True, fill='both')

		self.infoframe = tk.Frame(self.parent, bg='black', padx=8, pady=8, highlightthicknes=0)
		self.infoframe.place(relx=0.70, y=0, relwidth=0.30, relheight=0.90)
		self.infowin = tk.Text(self.infoframe, state='disabled', bg='black', fg='white', highlightbackground=frame_color, highlightthicknes=2)
		self.infowin.pack(expand=True, fill='both')

		self.commandframe = tk.Frame(self.parent, bg='black', padx=8, pady=8, highlightthicknes=0)
		self.commandframe.place(x=0, rely=0.90, relwidth=1.00, relheight=0.10)
		self.commandwin = tk.Text(self.commandframe, bg='black', fg='white', insertbackground='white', highlightcolor=frame_color, highlightbackground=frame_color, highlightthicknes=2)
		self.commandwin.tag_config('red', foreground='red')
		self.commandwin.pack(expand=True, fill='both')

		self.commandwin.focus_set()
		self.commandwin.insert('1.0', 'TasKey >> ', 'red')

		## BINDINGS ## 

		self.commandwin.bind('<FocusOut>', self.FocusReturn)

		self.commandwin.bind('<KeyRelease>', self.PromptProtect)

		self.commandwin.bind('<Return>', self.CommandReturn)


	def FocusReturn(self, event): 
		self.commandwin.focus_set()
		
	def PromptProtect(self, event):
		cursor_position = self.commandwin.index(tk.INSERT)
		[cursor_line, cursor_column] = cursor_position.split('.')
		if int(cursor_line) == 1:
			if int(cursor_column) < 10:
				self.commandwin.delete('1.0', '1.10')
				self.commandwin.insert('1.0', 'TasKey >> ', 'red')

	def CommandReturn(self, event):
		input_raw = self.commandwin.get('1.10', tk.END) # includes the erroneus '\n' at end
		input_stripped = input_raw[0:len(input_raw)-1] # ending '\n' stripped
		command = ComPro(self.settings, input_stripped)
		self.WindowManager(command)
		self.commandwin.delete('1.10', tk.END)
		return 'break'

	def WindowManager(self, command):
		
		if command[0] == 'info':
			self.infowin.configure(state='normal')
			self.infowin.delete('1.0', tk.END)
			alpha_index = command[1]
			index = AlphaIndexer(alpha_index, reverse=True)
			if self.current_win == 'main':
				target = DB_Retriever(index)
				output = [
					'Name: ' + target.name + '\n',
					'Priority: ' + target.priority + '\n',
					'Created: ' + str(target.created) + '\n',
					'Days Remaining: ' + str(target.remaining) + '\n',
					'Priority Score: ' + str(target.score) + '\n',
					'Footnote: ' + str(target.footnote) + '\n'
					]
				if target.hard_deadline:
					output.insert(2, 'Deadline: ' + str(target.deadline) + ' (Hard)' + '\n')
				else:
					output.insert(2, 'Deadline: ' + str(target.deadline) + ' (Auto)' + '\n')
			elif self.current_win == 'archive':
				target = DB_Retriever(index, in_archive=True)
				output = [
					'Name: ' + target.name + '\n',
					'Priority: ' + target.priority + '\n',
					'Occurred: ' + str(target.occurred) + '\n',
					'Reason: ' + target.reason + '\n',
					'Footnote: ' + str(target.footnote) + '\n'
					]
				if target.hard_deadline:
					output.insert(2, 'Deadline: ' + str(target.deadline) + ' (Hard)' + '\n')
				else:
					output.insert(2, 'Deadline: ' + str(target.deadline) + ' (Auto Generated)' + '\n')
			
			for i in range(len(output)):
				self.infowin.insert(tk.END, output[i])
			self.infowin.configure(state='disabled')
		

		if command[0] == 'main':
			self.current_win = 'main'
			self.current_sel = 'aa'
			self.listwin.configure(state='normal')
			self.listwin.delete('1.0', tk.END)
			size = DB_Size()
			for i in range(size):
				target = DB_Retriever(i)
				self.listwin.insert(tk.END, target.alpha_index + ' - ' + target.name + '\n')
			self.listwin.configure(state='disabled')
		if command[0] == 'archive':
			self.current_win = 'archive'
			self.current_sel = 'aa'
			self.listwin.configure(state='normal')
			self.listwin.delete('1.0', tk.END)
			size = DB_Size(check_archive=True)
			for i in range(size):
				target = DB_Retriever(i, in_archive=True)
				self.listwin.insert(tk.END, target.alpha_index + ' - ' + target.name + '\n')
			self.listwin.configure(state='disabled')
		
		if command[0] == 'settings':
			pass
		if command[0] == 'kill':
			SafeSaveDB(TaskDB, ArchiveDB)
			self.parent.destroy
			exit()
		
		if command[0] == None:
			if self.current_win == 'main':
				self.listwin.configure(state='normal')
				self.listwin.delete('1.0', tk.END)
				size = DB_Size()
				for i in range(size):
					target = DB_Retriever(i)
					self.listwin.insert(tk.END, target.alpha_index + ' - ' + target.name + '\n')
				self.listwin.configure(state='disabled')
			elif self.current_win == 'archive':
				self.current_win = 'archive'
				self.current_sel = 'aa'
				self.listwin.configure(state='normal')
				self.listwin.delete('1.0', tk.END)
				size = DB_Size(check_archive=True)
				for i in range(size):
					target = DB_Retriever(i, in_archive=True)
					self.listwin.insert(tk.END, target.alpha_index + ' - ' + target.name + '\n')
				self.listwin.configure(state='disabled')
		if command[0] == False:
			pass

