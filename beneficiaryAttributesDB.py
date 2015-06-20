import csv 
import os 
import json 

"""
   use the following keywords:  
   beneficiary - Beneficiary Summary Files 
   carrier - Carrier Claim Files 
   inpatient - Inpatient Claim Files 
   outpatient - Outpatient Claim Files 
   prescription - Prescription Drug Events 
""" 

keywords = {
	'beneficiary': 'Beneficiary_Summary_File',
	'carrier': 'Carrier_Claims', 
	'inpatient': 'Inpatient_Claims_Sample', 
 	'outpatient': 'Outpatient_Claims_Sample',
	'prescription': 'Prescription_Drug_Events'
	}

def getCMSFiles(directory, string):
	
	keywords = {
        'beneficiary': 'Beneficiary_Summary_File',
        'carrier': 'Carrier_Claims',
        'inpatient': 'Inpatient_Claims_Sample',
        'outpatient': 'Outpatient_Claims_Sample',
        'prescription': 'Prescription_Drug_Events'
        }
	
	try: 
		fileList = [] 	
		keywordFilter = keywords[string]  
		
		for file in os.listdir(directory): 
			if keywordFilter in file:
				fileList.append(file) 
			else:
				pass 
		return fileList 
	except: 
		return "Use this dictionary %s" % keywords


def buildBeneficiaryTable(list, directory, dumpToFile_Boolean): 
	beneficiaryDB = {} 
	
	for file in list:
		year = file[6:10]
		loc = directory + "/" + file 

		f = open(loc) 
		reader = csv.reader(f) 

		headers = reader.next() 
		desynpuf_id_index = headers.index('DESYNPUF_ID') 
		birth_date_index = headers.index('BENE_BIRTH_DT')
		sex_index = headers.index('BENE_SEX_IDENT_CD') 
		race_index = headers.index('BENE_RACE_CD') 
		state_index = headers.index('SP_STATE_CODE') 
		county_index = headers.index('BENE_COUNTY_CD') 
		
		diabetes_index = headers.index('SP_DIABETES') 
		heart_index = headers.index('SP_CHF') 
		
		for patient in reader:
			if patient[diabetes_index] == '1' or patient[heart_index] == '1':
				desynpuf_id = patient[desynpuf_id_index] 
				
				if desynpuf_id not in beneficiaryDB:
					beneficiaryDB[desynpuf_id] = {} 
					beneficiaryDB[desynpuf_id]['birth_date'] = patient[birth_date_index]
					beneficiaryDB[desynpuf_id]['sex'] = patient[sex_index]
					beneficiaryDB[desynpuf_id]['race'] = patient[race_index] 
					beneficiaryDB[desynpuf_id]['state'] = patient[state_index] 
					beneficiaryDB[desynpuf_id]['county'] = patient[county_index] 
					beneficiaryDB[desynpuf_id][year] = {}
					beneficiaryDB[desynpuf_id][year]['diabetes'] = patient[diabetes_index] 
					beneficiaryDB[desynpuf_id][year]['heart'] = patient[heart_index]  
				else:
					beneficiaryDB[desynpuf_id][year] = {}
					beneficiaryDB[desynpuf_id][year]['diabetes'] = patient[diabetes_index]
					beneficiaryDB[desynpuf_id][year]['heart'] = patient[heart_index]
			else:
				pass 

	if dumpToFile_Boolean:
		with open("beneficiaryDB.json", 'wb') as fp: 
			json.dump(beneficiaryDB, fp) 
	else: 
		return beneficiaryDB
				
if __name__=='__main__':
	directory = os.environ['health_path']
	files = getCMSFiles(directory, 'beneficiary')
	buildBeneficiaryTable(files, directory, True) 

