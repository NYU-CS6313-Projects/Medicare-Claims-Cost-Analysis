from diagnosis import getFiles
import csv


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
					if visit[all_diag[index]] not in summary:
						summary[visit[all_diag[index]]] = {}
						index += 1
					else:
						index += 1

	print len(summary.keys())


if __name__=='__main__':
	chronic = loadBeneficiary('patient_summary.csv')
	parsePatientFiles(li, chronic)
