# to correspond diagnoses with chronic conditions
# ie, "for X diagnosis, n1 patients with that diagnosis have chronic condition Y, n2 patients have chronic condition Z, etc."
import csv
import json

def readBenSum(file, diseases):
  patients = {}
  
  with open(file, "rb") as csvfile:
    beneficiaries = csv.reader(csvfile)
    headers = beneficiaries.next()
    
    patIndex = headers.index('DESYNPUF_ID')

    chronicIndices = {}
    chronicIndices["alzheimers"]    = headers.index('SP_ALZHDMTA')
    chronicIndices["heartFailure"]  = headers.index('SP_CHF')
    chronicIndices["kidney"]        = headers.index('SP_CHRNKIDN')
    chronicIndices["cancer"]        = headers.index('SP_CNCR')
    chronicIndices["COPD"]          = headers.index('SP_COPD')
    chronicIndices["depression"]    = headers.index('SP_DEPRESSN')
    chronicIndices["diabetes"]      = headers.index('SP_DIABETES')
    chronicIndices["ischemicHeart"] = headers.index('SP_ISCHMCHT')
    chronicIndices["osteo"]         = headers.index('SP_OSTEOPRS')
    chronicIndices["arthritis"]     = headers.index('SP_RA_OA')
    chronicIndices["stroke"]        = headers.index('SP_STRKETIA')

    for patient in beneficiaries:
      patID = patient[patIndex]
      patientChronic = []
      for i in diseases:
        if patient[chronicIndices[i]] == '1':
          patientChronic.append(i)
      patients[patID] = patientChronic
    
  return(patients)

def readClaims(file):
  diagCodes = {}  
  diagHeaders = ['ICD9_DGNS_CD_1', 'ICD9_DGNS_CD_2', 'ICD9_DGNS_CD_3', 'ICD9_DGNS_CD_4', 'ICD9_DGNS_CD_5', 'ICD9_DGNS_CD_6', 'ICD9_DGNS_CD_7', 'ICD9_DGNS_CD_8', 'ICD9_DGNS_CD_9', 'ICD9_DGNS_CD_10']
  
  with open(file, "rb") as csvfile:
    claims = csv.reader(csvfile)
    headers = claims.next()
    
    patIndex = headers.index('DESYNPUF_ID')

    diagIndices = []
    for i in range(10):
      diagIndices.append(headers.index(diagHeaders[i]))

    for claim in claims:
      patID = claim[patIndex]
      for i in diagIndices:
        diagnosis = claim[i]
        if diagnosis == "":
          pass
        else:
          if diagnosis not in diagCodes:
            diagCodes[diagnosis] = []
          if patID not in diagCodes[diagnosis]:
            diagCodes[diagnosis].append(patID)

  return(diagCodes)

def correspond(bens, diags):
  finalDict = {}

  for code in diags:
    finalDict[code] = {}
    patCount = 0
    for patID in diags[code]:
      patCount += 1
      for chronic in bens[patID]:
        if chronic not in finalDict[code]:
          finalDict[code][chronic] = 1
        else:
          finalDict[code][chronic] += 1
    finalDict[code]["totalCount"] = patCount

  return(finalDict)

def jsonDump(dict, writeFile):
  with open(writeFile, 'wb') as fp:
    json.dump(dict, fp)
  print "done writing", writeFile



if __name__=='__main__':

  #readfiles
  benSumFile = "DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv"
  inpatientFile = "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv"
  outpatientFile = "DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv"

  #writefiles
  ipWrite = "inpatientChronic.json"
  opWrite = "outpatientChronic.json"

  #chronic diseases
  chronicDis = ["alzheimers", "heartFailure", "kidney", "cancer", "COPD", "depression", "diabetes", "ischemicHeart", "osteo", "arthritis", "stroke"]

  #beneficiary summary operations
  benSum = readBenSum(benSumFile, chronicDis)

  #inpatient operations
  inpatient = readClaims(inpatientFile)
  ipCorr = correspond(benSum, inpatient)
  jsonDump(ipCorr, ipWrite)
  
  #outpatient operations  
  outpatient = readClaims(outpatientFile)
  opCorr = correspond(benSum, outpatient)
  jsonDump(opCorr, opWrite)
