from diagnosis import getFiles
import json
import csv
from datetime import datetime 


def loadSummary(file):
	with open(file, "rb") as jsonfile:
		summary = json.load(jsonfile)

		return summary


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


def parsePatientFiles(li, dictionary, summary_dictionary):
	summary = {} 
	all_chronic = ["alzheimers", "heartFailure", "kidney", "cancer", "COPD", "depression", "diabetes", "ischemicHeart", "osteo", "arthritis", "stroke"]

	for file in li: 
		f = open(file)
		reader = csv.reader(f) 
		headers = reader.next()

		patIndex = headers.index('DESYNPUF_ID')
		claimIndex = headers.index('CLM_PMT_AMT')
		
		proc1_index = headers.index('ICD9_PRCDR_CD_1')
		proc2_index = headers.index('ICD9_PRCDR_CD_2')
		proc3_index = headers.index('ICD9_PRCDR_CD_3')
		proc4_index = headers.index('ICD9_PRCDR_CD_4')
		proc5_index = headers.index('ICD9_PRCDR_CD_5')
		proc6_index = headers.index('ICD9_PRCDR_CD_6') 

		all_procs = [proc1_index, proc2_index, proc3_index, proc4_index, proc5_index, proc6_index]
		
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
			if float(visit[claimIndex]) <= 0:
				pass
			else:	
				index = 0 
				while index < 6: 
					if visit[all_procs[index]] == '':
						index = 6 
					else: 
						proc = visit[all_procs[index]]	
						if proc not in summary: 
							summary[proc] = {}
							summary[proc]['alzheimers'] = 0 
							summary[proc]['heartFailure'] = 0  
							summary[proc]['kidney'] = 0 
							summary[proc]['cancer'] = 0 
							summary[proc]['COPD'] = 0 
							summary[proc]['depression'] = 0 
							summary[proc]['diabetes'] = 0 
							summary[proc]['ischemicHeart'] = 0 
							summary[proc]['osteo'] = 0
                                                        summary[proc]['arthritis'] = 0
                                                        summary[proc]['stroke'] = 0
							summary[proc]['total_visits'] = 1 

							summary[proc]["uniques"] = [] 
							summary[proc]["uniques"].append(visit[patIndex]) 
							
							summary[proc]["total_cost"] = float(visit[claimIndex])

							for i, illness in enumerate(dictionary[visit[patIndex]]):
								if illness == '1.0':
									summary[proc][all_chronic[i]] += 1
								elif illness == '2.0':
									pass
								else:
									pass 										 
							
							## create dictionary containing the count of each diagnosis for each procedure 
							summary[proc]["diagnosis"] = {} 
							diag_index = 0 
							while diag_index < 10:
								diag = visit[all_diag[diag_index]]
								if diag == '':
									diag_index = 10 
								else: 
									summary[proc]["diagnosis"][diag] = 1
									diag_index += 1


						else:  
							summary[proc]["total_visits"] += 1
							summary[proc]["total_cost"] += float(visit[claimIndex])
							summary[proc]["uniques"].append(visit[patIndex])									

							for i, illness in enumerate(dictionary[visit[patIndex]]):
                                                                if illness == '1.0':
                                                                        summary[proc][all_chronic[i]] += 1
                                                                elif illness == '2.0':
                                                                        pass
                                                                else:
                                                                        pass
	
							diag_index = 0 
							while diag_index < 10:
								diag = visit[all_diag[diag_index]] 
								if diag == '':
									diag_index = 10
								else:
									if diag in summary[proc]["diagnosis"]:
										summary[proc]["diagnosis"][diag] += 1 
										diag_index += 1
									else: 
										summary[proc]["diagnosis"][diag] = 1
										diag_index += 1 
						index += 1

	for procedures in summary.items():
		summary[procedures[0]]["uniques"] = len(set(summary[procedures[0]]["uniques"]))			

	summary['total_uniques'] = summary_dictionary['allpatients']['total_uniques'] #change inpatients to other types for summary data
	summary['total_claims'] = summary_dictionary['allpatients']['total_claims']
	
	print len(summary), summary['total_claims'], summary['total_uniques']
	return summary
	#print len(summary), summary['total_claims'], summary['total_uniques']  
	#print summary['9904']

def createJson(dictionary):

	with open('procedures_allpatients.json', 'wb') as fp:
		json.dump(dictionary, fp)

	print "done in ", datetime.now() - startTime
											
if __name__=='__main__':
	startTime = datetime.now() 
	summary = loadSummary("summary.json") 
	chronic = loadBeneficiary("beneficiary.csv") 
	x, y = getFiles()
	x.extend(y) 
	dictionary = parsePatientFiles(x, chronic, summary)
	createJson(dictionary) 
 
