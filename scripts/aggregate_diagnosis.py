import json


def loadReference(jsonfile):
	f = open(jsonfile) 
	code_reference = json.load(f) 

	return code_reference 

def aggregateObservations(jsonfile, reference):
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

			if l2_label not in dictionary:
				dictionary[l2_label] = {}
				for key in chronic_data.iterkeys():
					dictionary[l2_label][key] = float(chronic_data[key])
			else:	
				for key in chronic_data.iterkeys():
					if key not in dictionary[l2_label]:
						dictionary[l2_label][key] = float(chronic_data[key])
					else:
						dictionary[l2_label][key] += float(chronic_data[key])				


	with open('l2code_outpatients.json', 'wb') as fp:
		json.dump(dictionary, fp)	
#{u'uniques': 90, u'cancer': 7, u'COPD': 29, u'osteo': 23, u'total_cost': 918000.0, u'arthritis': 22, u'ischemicHeart': 74, u'alzheimers': 43, u'stroke': 13, u'kidney': 47, u'heartFailure': 71, u'depression': 44, u'total_claims': 90, u'diabetes': 71}
	#[u'l3code', u'l2code', u'l3label', u'l2label', u'l4code', u'l1label', u'l1code', u'l4label']


if __name__=='__main__':
	code_reference = loadReference("diagnosisXwalk.json")
	aggregateObservations("../sp2015-group8/diagnosisJSONfiles/diagnosis_outpatients.json", code_reference) 
