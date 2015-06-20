import os 
import csv
import json 
import numpy  
from beneficiaryAttributesDB import getCMSFiles, buildBeneficiaryTable


def extractClaims(list, db):
	cnt = 0 
	for file in list: 
		loc = directory + "/" + file 
		f = open(loc) 
		reader = csv.reader(f) 

		headers = reader.next() 
		
		desynpuf_id_index = headers.index('DESYNPUF_ID')	
		clm_from_dt_index = headers.index("CLM_FROM_DT")
		clm_thru_dt_index = headers.index("CLM_THRU_DT") 
		clm_pmt_amt_index = headers.index("CLM_PMT_AMT") 
		clm_utlztn_cnt_index = headers.index('CLM_UTLZTN_DAY_CNT')
		
		for visit in reader:
			patientID = visit[desynpuf_id_index] 
			if patientID in db:
				print visit[clm_utlztn_cnt_index], visit[clm_pmt_amt_index]  	 
				cnt += 1 
			else: 
				print 'not in db' 

	print "HERE IS HOW MNAY OBS %s" % cnt 
if __name__=='__main__':
	directory = os.environ['health_path']
	files = getCMSFiles(directory, 'inpatient') 
	
	f = open("beneficiaryDB.json") 
	beneficiaryDB = json.load(f) 

	extractClaims(files, beneficiaryDB) 
