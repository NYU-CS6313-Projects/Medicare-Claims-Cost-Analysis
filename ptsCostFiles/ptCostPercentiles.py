import csv
import json
from beneficiaryORG import getFiles

def readBenSum(list):

  patientCosts = {}
  for item in list:
    loc = "../" + item  
    with open(loc, "rb") as csvfile:
      beneficiaries = csv.reader(csvfile)
      headers = beneficiaries.next()
    
      patIndex = headers.index('DESYNPUF_ID')
      inpatientCostIndex = headers.index('MEDREIMB_IP')
      outpatientCostIndex = headers.index('MEDREIMB_OP')
      carrierCostIndex = headers.index('MEDREIMB_CAR')

     ##patientCosts = {}

      for patient in beneficiaries:
        patID = patient[patIndex]
        inpatientCost = float(patient[inpatientCostIndex])
        outpatientCost = float(patient[outpatientCostIndex])
        carrierCost = float(patient[carrierCostIndex])
        totalCost = inpatientCost + outpatientCost + carrierCost
      # toggle here to eliminate 0 cost
        if totalCost > minCost:
          if patID in patientCosts:
            patientCosts[patID] += totalCost
          else:
            patientCosts[patID] = totalCost

  return (patientCosts)


def getPercentiles(ptCosts):
  ptCostList = []
  for i in ptCosts:
    ptCostList.append([i, ptCosts[i]])

  ptCostList.sort(key=lambda x: x[1])
  numPts = len(ptCosts)

  pctileDict = {}
  for i in range(100):
    pctileDict[i] = {}
    pctileDict[i]["patients"] = []
    reverseIndex = numPts*i/100
    pctileDict[i]["costFloor"] = ptCostList[reverseIndex][1]

  for i in range(len(ptCosts)):
    index = int(i*100/numPts)
    pctileDict[index]["patients"].append(ptCostList[i][0])

  # for i in pctileDict:
  #   print i, len(pctileDict[i]["patients"]), pctileDict[i]["costFloor"]

  return(pctileDict)


def jsonDump(dict, writeFile):
  with open(writeFile, 'wb') as fp:
    json.dump(dict, fp)
  print "done writing", writeFile


if __name__=='__main__':
  minCost = 0

  benSumFile = getFiles() 
  jsonWriteFile = "ptsByPercentile.json"

  ptCostDict = readBenSum(benSumFile)
  ptsByPercentile = getPercentiles(ptCostDict)
  jsonDump(ptsByPercentile, jsonWriteFile)
