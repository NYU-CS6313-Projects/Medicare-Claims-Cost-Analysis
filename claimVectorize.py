import os 
import csv
import json 
import numpy  
from beneficiaryAttributesDB import getCMSFiles, beneficiaryTable


def extractClaims(list):

	for file in list: 
		
	


if __name__=='__main__':
	directory = os.environ['health_path']
	files = getFiles(directory, 'inpatient') 
	
	f = open("beneficiaryDB.json") 
	beneficiaryDB = json.load(f) 

	newMethod(files0 
