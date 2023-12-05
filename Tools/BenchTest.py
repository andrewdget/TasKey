## NOTES ##
'''
1. need to set minimum 'nochar'
'''

## DEPENDENCIES ## 


## DEFINITIONS ##

def ASCII_ProgressBar(nochar, complete, of):
	progress = complete/of
	max_bars = nochar - 9
	no_bars = int(max_bars * progress)
	no_spaces = max_bars - no_bars

	if progress != 1:
		bar ='[' + '/'*no_bars + ' '*no_spaces + '] ' + ' ' + str(round(progress*100, 1)) + '%'
	else:
		bar ='[' + '/'*no_bars + ' '*no_spaces + '] ' + str(round(progress*100, 1)) + '%'
	
	return bar




## EXECUTABLE ## 

bar1 = ASCII_ProgressBar(55, 2, 2)
bar2 = ASCII_ProgressBar(55, 23, 48)
bar3 = ASCII_ProgressBar(55, 8, 10)


print()
print('Critical Tasks ' + bar1)
print('   Total Tasks ' + bar2)
print('  Weekly Tasks ' + bar3)
print()

print(round(22.343, 1))