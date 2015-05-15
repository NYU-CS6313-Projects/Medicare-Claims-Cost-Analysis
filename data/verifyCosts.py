from diagnosis import getFiles
import csv 
import sys 

def checkTotalCost(list, diagnosisCode): 
	
	frequency = 0 
	total_cost = 0 

	for file in list: 
		print "looking through %s" % file 
		f = open(file) 
		reader = csv.reader(f) 

		headers = reader.next() 

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

		#"78606"			
		for visit in reader: 
			if float(visit[claimIndex]) <= 0:
				pass 
			else:
				index = 0 
				while index < 10:
                                        if visit[all_diag[index]] == '':
                                                index = 10
					elif visit[all_diag[index]] != diagnosisCode:
						pass 
					else: 
						total_cost += float(visit[claimIndex])
						frequency += 1		
					index += 1 
		
	print "%s has a total cost of %d and %d many times." % (diagnosisCode, total_cost, frequency) 
 
					
if __name__=='__main__':
	x, y = getFiles()
	z = x + y 
	file_type = sys.argv[1]
	
	if file_type == 'inpatients': 	
		checkTotalCost(x, str(sys.argv[2])) 
	elif file_type == 'outpatients': 
		checkTotalCost(y, str(sys.argv[2]))
	elif file_type == 'allpatients':
		checkTotalCost(z, str(sys.argv[2]))
	else:
		print "Please a files type (inpatients, outpatients, allpatients) and diagnosis code" 
		

