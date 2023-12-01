## NOTES ##
'''
1. add archive/backup option? Setting to prevent the deltion of (valid) old 
	savestates? Maybe add '-A' flag at end?
'''

## DEPENDENCIES ##
import os
import glob
import time
import pickle

## DEFINITIONS ##

def GetCreationTime(file):
	nochars = len(file)
	time = float(file[17:nochars-6].replace('-', '.'))
	return time


def Prune(archive=True):
	rootdir = os.getcwd()
	os.chdir(rootdir + '/Data')
	files = glob.glob('TasKey_Savestate_*.txt')
	valid = []
	remove = []
	for f in files:
		nochars = len(f)
		flag = f[nochars-6:nochars-4]
		if flag != '-V':
			remove.append(f)
		else: 
			valid.append(f)
	valid.sort(key=GetCreationTime, reverse=True)
	if archive == False:
		remove.extend(valid[1:])
	for f in remove:
		os.remove(f)
	os.chdir(rootdir)
	

def SafeLoadDB():
	rootdir = os.getcwd()
	os.chdir(rootdir + '/Data')
	files = glob.glob('TasKey_Savestate_*-V.txt')
	if len(files) != 0:
		files.sort(key=GetCreationTime, reverse=True)
		with open(files[0], 'rb') as f:
			database = pickle.load(f)
		TaskDB = database[0]
		ArchiveDB = database[1]
	else:
		TaskDB = []
		ArchiveDB = []
	os.chdir(rootdir)
	return TaskDB, ArchiveDB


def SafeSaveDB(TaskDB, ArchiveDB):
	rootdir = os.getcwd()
	os.chdir(rootdir + '/Data')
	old_savestate = glob.glob('TasKey_Savestate_*.txt')
	database = [TaskDB, ArchiveDB]
	tag = str(time.time()).replace('.', '-')
	filename = 'TasKey_Savestate_' + tag + '.txt'
	with open(filename, 'wb') as f:
		pickle.dump(database, f)
	status = True
	try:
		with open(filename, 'rb') as f:
			test = pickle.load(f)
	except:
		status = False
		return status
	if len(TaskDB) == len(test[0]):
		for i in range(len(TaskDB)):
			if TaskDB[i].__dict__ != test[0][i].__dict__:
				status = False
		if len(ArchiveDB) == len(test[1]):
			for i in range(len(ArchiveDB)):
				if ArchiveDB[i].__dict__ != test[1][i].__dict__:
					status = False
		else:
			status = False
	else:
		status = False
	if status == True:
		os.rename(filename, 'TasKey_Savestate_' + tag + '-V.txt')
	os.chdir(rootdir)
	return status


