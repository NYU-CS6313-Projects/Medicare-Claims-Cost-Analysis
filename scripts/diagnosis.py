import csv
import sys
import json
import os 

inpatient_files = []
outpatient_files = [] 

def getFiles():
	for i in os.listdir('/home/cusp/kl1771/cms_files/'):
		if 'Inpatient_Claims_Sample' in i:
			inpatient_files.append(i)  
		elif 'Outpatient_Claims_Sample' in i:
			outpatient_files.append(i)
		else:
			pass
	master = [] 
	master.append(inpatient_files) 
	master.append(outpatient_files)
	return master

def getUniques():
	x, y = getFiles() 
	z = x + y 
	 
	#x is all inpatient files
	#y is all outpatient files 
	#z is all patients merged  

	types = [x, y, z] 
	uniques = []
	names = ['inpatients', 'outpatients', 'allpatients'] 
	summary = {}  
	 
	for i, list in enumerate(types):
		uniques = []
		claims = []   
		for file in list:
			f = open(file)
			reader = csv.reader(f)
			reader.next() 
			for line in reader:
				uniques.append(line[0])
				claims.append(line[1]) 

		summary[names[i]] = {}
		summary[names[i]]['total_uniques'] = len(set(uniques))
		summary[names[i]]['total_claims'] = len(set(claims)) 
	
	with open('summary.json', 'wb') as fp:
		json.dump(summary, fp)		

