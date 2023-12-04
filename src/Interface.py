## NOTES ##
'''
1. remove executable seciton once done developing
2. implement sytle tags (in general and for command line)
3. develop method for highlighting tags

'''

## DEPENDENCIES ## 

import tkinter as tk
import tkinter.font as tkf
import pyfiglet

## DEFINITIONS ##

class TasKeyUI:
	def __init__(self, version, config, paths):
		self.version = version
		self.paths = paths

		self.current_win = 'Tasks'
		self.current_tab = list(self.paths.keys())[0]
		self.current_sel = 'aa'

		# import styles from config
		self.background_color = config['background_color']
		self.accent_color = config['accent_color']
		self.trim_color = config['trim_color']
		self.highlight_color = config['highlight_color']
		self.text_color = config['text_color']

		hlt = 0 # "1" places box around frames or "naked" text boxes, for debugging

		self.root = tk.Tk()

		self.root_height = self.root.winfo_height()
		self.root_width = self.root.winfo_width()

		self.root.title('TasKey ' + self.version + ' (Beta)')
		self.root.configure(height=600, width=1200, bg=self.background_color)


		# generate "TasKey" ASCII header and version subheader
		self.header = tk.Text(self.root)
		self.header.config(
			bg=self.background_color,
			fg=self.accent_color,
			highlightthicknes=hlt,
			height=5,
			width=29
			)
		self.header.place(x=10, y=10)
		self.ASCII_name = pyfiglet.figlet_format('TasKey', font='smslant')
		self.header.insert('1.0', self.ASCII_name)
		self.header.config(state='disabled')
		
		self.subheader = tk.Text(self.root)
		self.subheader.config(
			bg=self.background_color,
			fg=self.accent_color,
			highlightbackground=self.accent_color,
			highlightthicknes=1,
			font='Courier',
			padx=5,
			height = 4,
			width=3
			) 
		self.subheader.place(x=225, y=23)
		self.subheader.insert('1.0', self.version)
		self.subheader.config(state='disabled')


		# generate list display frame/window
		self.listframe = tk.Frame(self.root)
		self.listframe.config(
			bg=self.background_color,
			highlightthicknes=hlt,
			)
		self.listframe.place(x=10, y=85, height=505, width=585)

		self.listwin = tk.Text(self.listframe)
		self.listwin.config(
			bg=self.background_color,
			fg=self.text_color,
			highlightbackground=self.trim_color,
			highlightthicknes=2,
			state='disabled'
			)
		self.listwin.pack(expand=True, fill='both')


		# generate info display frame/window
		self.infoframe = tk.Frame(self.root)
		self.infoframe.config(
			bg=self.background_color,
			highlightthicknes=hlt,
			)
		self.infoframe.place(x=605, y=300, height=230, width=585)

		self.infowin = tk.Text(self.infoframe)
		self.infowin.config(
			bg=self.background_color,
			fg=self.text_color,
			highlightbackground=self.trim_color,
			highlightthicknes=2,
			state='disabled'
			)
		self.infowin.pack(expand=True, fill='both')


		# generate commandline frame/window
		self.commandframe = tk.Frame(self.root)
		self.commandframe.config(
			bg=self.background_color,
			highlightthicknes=hlt,
			)
		self.commandframe.place(x=10, y=540, height=50, width= 1180)

		self.commandwin = tk.Text(self.commandframe)
		self.commandwin.config(
			bg=self.background_color,
			fg=self.text_color,
			insertbackground=self.text_color,
			highlightcolor=self.trim_color,
			highlightbackground=self.trim_color,
			highlightthicknes=2,
			font='Courier'
			)
		self.commandwin.pack(expand=True, fill='both')
		self.commandwin.focus_set()
		self.commandwin.insert('1.0', 'TasKey >> ')


		# generate tab display window
		self.tabwin = tk.Text(self.root)
		self.tabwin.config(
			bg=self.background_color,
			fg=self.text_color,
			highlightthicknes=hlt,
			font='Courier',
			wrap=tk.NONE
			)
		self.tabwin.place(x=285, y=35, height=45, width=905)
		self.RefreshTabs()


		# generate gadgets frame
		self.gadgetframe = tk.Frame(self.root)
		self.gadgetframe.config(
			bg=self.background_color,
			highlightthicknes=hlt
			)
		self.gadgetframe.place(x=605, y=85, width=585, height=206)


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
				self.commandwin.insert('1.0', 'TasKey >> ')


	def OnResize(self, event):
		self.root_height = self.root.winfo_height()
		self.root_width = self.root.winfo_width()

		self.listframe.place(
			x=10,
			y=85, 
			height=self.root_height-155,
			width=self.root_width/2 - 15
			)

		self.infoframe.place(
			x=self.root_width/2 + 5,
			y=300,
			height=self.root_height-370,
			width=self.root_width/2 - 15 
			)

		self.commandframe.place(
			x=10,
			y=self.root_height-60,
			height=50,
			width=self.root_width-20
			)

		self.tabwin.place(
			x=285,
			y=35,
			height=45,
			width=self.root_width-295
			)
		self.RefreshTabs()

		self.gadgetframe.place(
			x=self.root_width/2 + 5,
			y=85,
			height=206,
			width=self.root_width/2 - 15
			)


	def RefreshTabs(self):
		path_names = list(self.paths.keys())
		line1 = ''
		line2 = ''
		for name in path_names:
			nochars = len(name)
			line1 = line1 + ' ' + '_'*nochars + ' '
			line2 = line2 + '/'+name+'\\'
		tabs = line1 + '\n' + line2
		self.tabwin.delete('1.0', tk.END)
		self.tabwin.insert('1.0', tabs)

		charwidth = tkf.Font(font='Courier').measure('/')
		maxchar = int((self.root_width-295)/charwidth - 1)

		# insures backslashes are at least as long as tabs, even when wrapped
		if len(line2) > maxchar:
			self.tabwin.insert('3.0', '\n' + '\\'*len(line2))
		else:
			self.tabwin.insert('3.0', '\n' + '\\'*maxchar)


## EXECUTABLE ## 

version = 'v- 00.05.06'

paths = {
   'Main': '/some/junk/goes/here',
   'S1': '/some/junk/goes/here',
   'Dogs': '/some/junk/goes/here',
   'Long Test': '/some/junk/goes/here',
   'Anotha One': '/some/junk/went/here'
}

config = {
	'background_color': 'black',
	'accent_color': 'orange',
	'trim_color': 'grey40',
	'highlight_color': 'red',
	'text_color': 'white'
	}

TasKeyUI(version, config, paths)

