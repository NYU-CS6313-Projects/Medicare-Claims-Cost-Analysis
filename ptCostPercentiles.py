import csv
import json


def readBenSum(file):
  
  with open(file, "rb") as csvfile:
    beneficiaries = csv.reader(csvfile)
    headers = beneficiaries.next()
    
    patIndex = headers.index('DESYNPUF_ID')
    inpatientCostIndex = headers.index('MEDREIMB_IP')
    outpatientCostIndex = headers.index('MEDREIMB_OP')
    carrierCostIndex = headers.index('MEDREIMB_CAR')

    patientCosts = []

    for patient in beneficiaries:
      patID = patient[patIndex]
      inpatientCost = float(patient[inpatientCostIndex])
      outpatientCost = float(patient[outpatientCostIndex])
      carrierCost = float(patient[carrierCostIndex])
      totalCost = inpatientCost + outpatientCost + carrierCost
      patientCosts.append((patID, totalCost))

  return (patientCosts)


def getPercentiles(ptCosts):

  ptCosts.sort(key=lambda x: x[1])
  numPts = len(ptCosts)

  pctileDict = {}
  for i in range(100):
    pctileDict[i] = {}
    pctileDict[i]["patients"] = []
    reverseIndex = numPts*i/100
    pctileDict[i]["costFloor"] = ptCosts[reverseIndex][1]

  for i in range(len(ptCosts)):
    index = int(i*100/numPts)
    pctileDict[index]["patients"].append(ptCosts[i][0])

  # for i in pctileDict:
  #   print i, len(pctileDict[i]["patients"]), pctileDict[i]["costFloor"], "\n"

  return(pctileDict)


def jsonDump(dict, writeFile):
  with open(writeFile, 'wb') as fp:
    json.dump(dict, fp)
  print "done writing", writeFile


if __name__=='__main__':

  benSumFile = "DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv"
  jsonWriteFile = "ptsByPercentile.json"

  ptCostList = readBenSum(benSumFile)
  ptsByPercentile = getPercentiles(ptCostList)
  jsonDump(ptsByPercentile, jsonWriteFile)