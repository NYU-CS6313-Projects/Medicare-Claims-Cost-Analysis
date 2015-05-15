from diagnosis import getFiles
import csv 
import sys
import json  

def loadReference(file):
	f = open(file) 
	data = json.load(f) 
	return data 
	
def groupTotalCost(file, reference, l1code):
	f = open(file) 
	data = json.load(f) 
	
	total_cost = 0 
	for item in data.items():
		if item[0] == l1code: 
			cost = float(item[1]['total_cost'])
			
	
	
 
					
if __name__=='__main__':
	file = "diagnosisJSONfiles/diagnosis_inpatients.json" 
	reference = loadReference("diagnosisXwalk.json")
	l1code = str(sys.argv[1])
	groupTotalCost(file, reference, l1code)  		

