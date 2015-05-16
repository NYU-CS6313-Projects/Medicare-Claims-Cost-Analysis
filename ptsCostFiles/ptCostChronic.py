import csv
import json
from beneficiaryORG import getFiles

def readBenSum(list, chronics):

  patientStuff = {} 
  for item in list: 
    loc = "../" + item  
    with open(loc, "rb") as csvfile:
      beneficiaries = csv.reader(csvfile)
      headers = beneficiaries.next()
    
      patIndex = headers.index('DESYNPUF_ID')

      inpatientCostIndex = headers.index('MEDREIMB_IP')
      outpatientCostIndex = headers.index('MEDREIMB_OP')
      carrierCostIndex = headers.index('MEDREIMB_CAR')

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

      #patientStuff = {}

      for patient in beneficiaries:
        patID = patient[patIndex]
        inpatientCost = float(patient[inpatientCostIndex])
        outpatientCost = float(patient[outpatientCostIndex])
        carrierCost = float(patient[carrierCostIndex])
        totalCost = inpatientCost + outpatientCost + carrierCost
      # toggle here to eliminate 0 cost
        if totalCost > minCost:
          if patID not in patientStuff:
            patientStuff[patID] = {"cost": totalCost}
            patientChronic = []
            for i in chronics:
              if patient[chronicIndices[i]] == '1':
                patientChronic.append(i)
            patientStuff[patID]["chronics"] = patientChronic
          else:
            patientStuff[patID]["cost"] += totalCost
            for i in chronics:
              if patient[chronicIndices[i]] == '1':
                if i not in patientStuff[patID]["chronics"]:
                  patientStuff[patID]["chronics"].append(i)

  return (patientStuff)


def jsonDump(dict, writeFile):
  with open(writeFile, 'wb') as fp:
    json.dump(dict, fp)
  print "done writing", writeFile


if __name__=='__main__':
  minCost = 0
  chronicDis = ["alzheimers", "heartFailure", "kidney", "cancer", "COPD", "depression", "diabetes", "ischemicHeart", "osteo", "arthritis", "stroke"]

  benSumFile = getFiles() 
  jsonWriteFile = "ptCostChronic.json"

  ptStuffList = readBenSum(benSumFile, chronicDis)
  # for i in ptStuffList:
  #   print i, ptStuffList[i]["cost"], ptStuffList[i]["chronics"]

  jsonDump(ptStuffList, jsonWriteFile)
