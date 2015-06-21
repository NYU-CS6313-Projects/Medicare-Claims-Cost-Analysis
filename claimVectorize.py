import os 
import csv
import json 
import numpy  
from beneficiaryAttributesDB import getCMSFiles, buildBeneficiaryTable


def extractClaims(list, db):
	data = [] 
	counterClaims = {} 

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
		
		"""we are only summing the number diagnosis received by the patient 
		   per visits""" 
		
		diag1_index = headers.index('ICD9_DGNS_CD_1')
        	diag2_index = headers.index('ICD9_DGNS_CD_2')
        	diag3_index = headers.index('ICD9_DGNS_CD_3')
        	diag4_index = headers.index('ICD9_DGNS_CD_4')
        	diag5_index = headers.index('ICD9_DGNS_CD_5')
        	diag6_index = headers.index('ICD9_DGNS_CD_6')
        	diag7_index = headers.index('ICD9_DGNS_CD_7')
        	diag8_index = headers.index('ICD9_DGNS_CD_8')
        	diag9_index = headers.index('ICD9_DGNS_CD_9')
        	diag10_index = headers.index('ICD9_DGNS_CD_10')

		diagList = [diag1_index, diag2_index, diag3_index, diag4_index, diag5_index, diag6_index, diag7_index, diag8_index, diag9_index, diag10_index]

		for visit in reader:

			patientID = visit[desynpuf_id_index] 
			claimAmount = visit[clm_pmt_amt_index]
			claimStartDate = visit[clm_from_dt_index] 
			lengthOfStay = visit[clm_utlztn_cnt_index] 
			
			if clm_from_dt_index != '' and claimStartDate != '':	
							
				index = 0 
				diagnosisCount = 0  		
		
				while index < 10:
					if visit[diagList[index]] != '': 
						diagnosisCount += 1 
						index += 1
					else:
						index = 10 			
		
				if patientID in db:
					rowData = [patientID, float(claimAmount), int(claimStartDate), int(lengthOfStay), diagnosisCount]
					data.append(rowData) 
					
					if patientID not in counterClaims: 	
						counterClaims[patientID] = {}
						if lengthOfStay == '':
							lengthOfstay = 1 
							counterClaims[patientID][claimStartDate] = lengthOfStay
						else:
							counterClaims[patientID][claimStartDate] = int(lengthOfStay)
					else:
						if lengthOfStay == '':
							lengthOfstay = 1
							counterClaims[patientID][claimStartDate] = lengthOfStay
						else:
							counterClaims[patientID][claimStartDate] = int(lengthOfStay) 
				else:
					pass
			else:
				pass  

	#for k, v in counterClaims.items():
	#	for i in counterClaims[k].values():
	#		if type(i) is str:
	#			print counterClaims[k]
	#			print 'HIGHLIGHT >>>>>>>>>>>>>'
	#		else:
	#			print counterClaims[k] 
	
	for row in data:
	
		patientID = row[0] 
		claimDate = row[2]
		claimYear = str(claimDate)[0:4] 
	 
		hospitalDays = sum([v for k, v in counterClaims[patientID].items() if k <= claimDate]) 
		admissionsTo = len([v for k, v in counterClaims[patientID].items() if k <= claimDate])
		       
		row.append(hospitalDays) 
		row.append(admissionsTo) 
		
		try:		
			row.append(int(db[patientID]["sex"]))
			row.append(int(db[patientID]["county"]))
			row.append(int(db[patientID]["state"]))
			row.append(int(db[patientID]["race"]))
			row.append(int(db[patientID]["birth_date"]))

			row.append(int(db[patientID][claimYear]["heart"]))
			row.append(int(db[patientID][claimYear]["diabetes"])) 

			print row 
		except:
			pass 
 
if __name__=='__main__':
	directory = os.environ['health_path']
	files = getCMSFiles(directory, 'inpatient')[0:5]  
	
	f = open("beneficiaryDB.json") 
	beneficiaryDB = json.load(f) 
	dict = {} 
	extractClaims(files, beneficiaryDB) 
