import json


def loadReference(jsonfile):
	f = open(jsonfile) 
	code_reference = json.load(f) 

	return code_reference

def loadUniqueClaims(jsonfile): 
	f = open(jsonfile)
	claims_file = json.load(f) 

	return claims_file  

def aggregateObservations(jsonfile, claims_link, reference):
	f = open(jsonfile)
	observations = json.load(f) 
	
	dictionary = {} 
	
	for diagnosis in observations.items():
		diag_code = diagnosis[0]
		chronic_data = diagnosis[1]

		if diag_code == 'total_claims' or diag_code == 'total_uniques':
			pass
		else:
			try:
				l2_label = reference[diag_code]['l2label']
				l2_code = reference[diag_code]['l2code']
			except:
				pass

			if l2_code not in dictionary:
				dictionary[l2_code] = {}
				dictionary[l2_code]['l2_label'] = l2_label ### add l1_label for reference
				for key in chronic_data.iterkeys():
					dictionary[l2_code][key] = float(chronic_data[key])
			
				dictionary[l2_code]["unique_claims"] = [] 
				dictionary[l2_code]["unique_claims"].extend(claims_link[diag_code]['claims']) 
			
				dictionary[l2_code]["unique_patients"] = [] 
				dictionary[l2_code]["unique_patients"].extend(claims_link[diag_code]['patients'])

			else:	
				for key in chronic_data.iterkeys():
					if key not in dictionary[l2_code]:
						dictionary[l2_code][key] = float(chronic_data[key])
					else:
						dictionary[l2_code][key] += float(chronic_data[key])				
				
				dictionary[l2_code]["unique_claims"].extend(claims_link[diag_code]['claims'])
				dictionary[l2_code]["unique_patients"].extend(claims_link[diag_code]['patients'])				


	for i in dictionary.items():
		del dictionary[i[0]]["total_claims"] 
		del dictionary[i[0]]["uniques"]

		dictionary[i[0]]["unique_patients"] = len(set(i[1]["unique_patients"]))
		dictionary[i[0]]["unique_claims"] = len(set(i[1]["unique_claims"]))

	with open('l2code_allpatients.json', 'wb') as fp:
		json.dump(dictionary, fp)	

if __name__=='__main__':
	code_reference = loadReference("diagnosisXwalk.json")
	claims_link = loadUniqueClaims("scripts/allpatient_claims_unique.json") 
	aggregateObservations("../sp2015-group8/data/diagnosisJSONfiles/diagnosis_allpatients.json", claims_link, code_reference) 
