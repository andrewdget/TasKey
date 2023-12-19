## NOTES ##
'''
paths = {DBname: DBpath}

load paths
find latest file w/ the given name @ path
append to DBroster dict

UI can then load DB by name from roster
'''

## DEPENDENCIES ## 

import os
import glob
import pickle
import time

from DataStructure import *

## DEFINITIONS ##

def GetFiles(name):
	header = 'TKsavestate_' + name + '_'
	files_unsorted = glob.glob(header + '*.txt')
	times = []
	for file in files_unsorted:
		time = file.replace(header, '').replace('-','.').replace('.txt', '')
		times.append(float(time))
	times.sort(reverse=True)

	files = []
	for time in times:
		time = str(time).replace('.', '-')
		for file in files_unsorted:
			if time in file:
				files.append(file)
	
	return files


def LoadDB(config, name, path):
	rootdir = os.getcwd()
	os.chdir(path)
	files = GetFiles(name)
	if len(files) == 0:
		DB = TaskDB(config, name, path)
	else:
		with open(files[0], 'rb') as f:
			DB = pickle.load(f)
	os.chdir(rootdir)
	return DB


def SafeSaveDB(DB):
	name = DB.db_name
	path = DB.path
	rootdir = os.getcwd()

	os.chdir(path)
	filename = 'TKsavestate_' + name + '_temp.txt'
	with open(filename, 'wb') as f:
		pickle.dump(DB, f)
	proceed = True
	try:
		with open(filename, 'rb') as f:
			test = pickle.load(f)
	except:
		proceed = False
		return proceed

	if len(DB.Active) == len(test.Active):
		for i in range(len(DB.Active)):
			if DB.Active[i].__dict__ != test.Active[i].__dict__:
				proceed = False
				return proceed
	else:
		proceed = False
		return proceed

	if len(DB.Archive) == len(test.Archive):
		for i in range(len(DB.Archive)):
			if DB.Archive[i].__dict__ != test.Archive[i].__dict__:
				proceed = False
				return proceed
	else:
		proceed = False
		return proceed

	if proceed == True:
		tag = str(time.time()).replace('.', '-')
		os.rename(filename, 'TKsavestate_' + name + '_' + tag + '.txt')

	os.chdir(rootdir)
	return proceed


def BatchLoadDB(config, path_roster):
	DBroster = {}
	names = list(path_roster.keys())
	for name in names:
		path = path_roster[name]
		DB = LoadDB(config, name, path)
		DBroster[name] = DB
	return DBroster


def BatchSafeSaveDB(DBroster):
	names = list(DBroster.keys())
	for name in names:
		DB = DBroster[name]
		state = SafeSaveDB(DB)
		if state == False:
			print('!! ERROR OCCURED DURING ATTEMPT TO SAVESTATE !!')


## EXECUTABLE ##
