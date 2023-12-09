## NOTES ##
'''

'''

## DEPENDENCIES ## 
import tkinter as tk

## DEFINITIONS ##


## EXECUTABLE ## 

root = tk.Tk()

target = tk.Text(root)
target.config(
	bg='black',
	height=3,
	width=150
	)
target.pack()

target.tag_config('green', foreground='green')
target.tag_config('orange', foreground='orange')
target.tag_config('red', foreground='red')


complete = 100
of = 100
bar = '/'*complete + '-'*(of-complete)

target.insert(tk.END, 'Critical Tasks [')
for i in range(len(bar)):
	char = bar[i]
	if char == '/':
		if i < 24:
			target.insert(tk.END, char, 'red')
		elif i < 49:
			target.insert(tk.END, char, 'orange')
		else:
			target.insert(tk.END, char, 'green')
	else:
		target.insert(tk.END, char)
target.insert(tk.END, ']')


root.mainloop()