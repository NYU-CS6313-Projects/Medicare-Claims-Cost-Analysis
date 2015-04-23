from diagnosis import getFiles 
import csv 
from datetime import datetime
startTime = datetime.now()

li = ['DE1_0_2008_to_2010_Outpatient_Claims_Sample_10.csv', 'DE1_0_2008_to_2010_Outpatient_Claims_Sample_11.csv']

def loadBeneficiary(file): 
	with open(file, "rb") as csvfile:
		beneficiaries = csv.reader(csvfile)
		headers = beneficiaries.next() 
		
		patIndex = headers.index('DESYNPUF_ID')
		chronicIndices = {} 
				
		for patient in beneficiaries: 
			chronicIndices[patient[patIndex]] = []
			[chronicIndices[patient[patIndex]].append(patient[i]) for i in range(1, 12)]
		
		return chronicIndices 		

	

def parsePatientFiles(li, dictionary):
	summary = {} 
	total_uniques = set([])
	all_chronic = ["alzheimers", "heartFailure", "kidney", "cancer", "COPD", "depression", "diabetes", "ischemicHeart", "osteo", "arthritis", "stroke"] 	

	for file in li:
		f = open(file) 
		reader = csv.reader(f)
		headers = reader.next()

		patIndex = headers.index('DESYNPUF_ID')
		claimIndex = headers.index('CLM_PMT_AMT') 
		
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

		all_diag = [diag1_index, diag2_index, diag3_index, diag4_index, diag5_index, diag6_index, diag7_index, diag8_index, diag9_index, diag10_index]
	
		for visit in reader: 
			index = 0 
			while index < 10:
				if visit[all_diag[index]] == '':
					index += 1 
				else:
					diag = visit[all_diag[index]]
					if diag not in summary:
						summary[diag] = {}
						summary[diag]["alzheimers"] = 0 
						summary[diag]["heartFailure"] = 0										
						summary[diag]["kidney"] = 0 
						summary[diag]["cancer"] = 0 
						summary[diag]["COPD"] = 0 
						summary[diag]["depression"] = 0 
						summary[diag]["diabetes"] = 0 
						summary[diag]["ischemicHeart"] = 0 
						summary[diag]["osteo"] = 0 	
						summary[diag]["arthritis"] = 0 
						summary[diag]["stroke"] = 0 	
						summary[diag]["total_visits"] = 1
						summary[diag]["uniques"] = []
						summary[diag]["uniques"].append(visit[patIndex])	
						#print summary[diag]["uniques"]

						for i, illness in enumerate(dictionary[visit[patIndex]]):
							if illness == '1.0': 
								summary[diag][all_chronic[i]] += 1 
							elif illness == '2.0':
								pass 
							else:
								pass  
								
					else:
						summary[diag]["total_visits"] += 1
						
						summary[diag]["uniques"].append(visit[patIndex])
						#print summary[diag]["uniques"]				
	
						for i, illness in enumerate(dictionary[visit[patIndex]]):
                                                        if illness == '1.0':
                                                                summary[diag][all_chronic[i]] += 1
                                                        elif illness == '2.0':
                                                                pass
                                                        else:
                                                                pass
					index += 1 	
				#	print diag, summary[diag] 
	cnt = 0 
	for diagnosis in summary.items():
		print cnt 
		cnt += 1 
		summary[diagnosis[0]]["uniques"] = len(set(summary[diagnosis[0]]["uniques"]))

	print summary
	print datetime.now() - startTime									
	


if __name__=='__main__':
	chronic = loadBeneficiary('patient_summary.csv') 
	x, y = getFiles()
	x.extend(y) 
	parsePatientFiles(x, chronic)	





