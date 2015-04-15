import csv
import sys
import json

def inputParse(file):
	f = open(file)	
	reader = csv.reader(f)
	headers = reader.next() 

	summary = {} 

	pat_index = headers.index('DESYNPUF_ID')
	claim_index = headers.index('CLM_PMT_AMT')

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

	all_chronic = [diag1_index, diag2_index, diag3_index, diag4_index, diag5_index, diag6_index, diag7_index, diag8_index, diag9_index, diag10_index]
	 
	for visit in reader:
		index = 0 

		while index < 9:
			if visit[all_chronic[index]] == '':
				pass
			else:
				# print visit[pat_index], visit[all_chronic[index]], visit[claim_index]
				visit_diag = visit[all_chronic[index]]
				if visit_diag not in summary: 
					summary[visit_diag] = {} 
					summary[visit_diag]['unique_patients'] = [] 
					summary[visit_diag]['unique_patients'].append(visit[pat_index])
					summary[visit_diag]['total_visits'] = 1
					summary[visit_diag]['total_costs'] = float(visit[claim_index])
				else:

					#if visit[pat_index] in summary[visit_diag]['unique_patients']:
					# 	pass
					# else:
					summary[visit_diag]['unique_patients'].append(visit[pat_index])
					summary[visit_diag]['total_visits'] += 1
					summary[visit_diag]['total_costs'] += float(visit[claim_index])

			index += 1 
			
	return summary

def getUniques(dictionary, name_of_file):
	for disease in dictionary.items():
		disease[1]['unique_patients'] = len(set(disease[1]['unique_patients']))


	with open(name_of_file, 'wb') as fp:
		json.dump(dictionary, fp)
		print "done"
		# print disease
		# print disease[1]['unique_patients'], disease[1]['total_visits']

if __name__=='__main__':
	initial_data = sys.argv[1] 
	name = sys.argv[2]
	inpatient_data = inputParse(initial_data)
	getUniques(inpatient_data, name)

	

