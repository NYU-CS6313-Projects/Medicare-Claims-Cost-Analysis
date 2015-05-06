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

    patientCosts = {}

    for patient in beneficiaries:
      patID = patient[patIndex]
      inpatientCost = float(patient[inpatientCostIndex])
      outpatientCost = float(patient[outpatientCostIndex])
      carrierCost = float(patient[carrierCostIndex])
      totalCost = inpatientCost + outpatientCost + carrierCost
      if totalCost >= minCost:
        patientCosts[patID] = totalCost

  return (patientCosts)

def makeHistogram(ptCosts):
  top = max(ptCostList.values())
  bottom = min(ptCostList.values())
  theRange = top-bottom
  numBins = 20
  binWidth = int(theRange/numBins)

  histDict = {}
  for i in range(numBins):
    binFloor = i*binWidth+minCost
    binCeiling = (i+1)*binWidth+minCost
    tempIDs = []
    for pt in ptCostList:
        tempCost = ptCostList[pt]
        if i == numBins-1:
            if (tempCost >= binFloor):
                tempIDs.append(pt)
        else:
            if (tempCost >= binFloor) and (tempCost < binCeiling):
                tempIDs.append(pt)
    histDict[i] = {"floor": binFloor, "ceiling": binCeiling, "length": len(tempIDs), "pts": tempIDs}
    # histDict[binFloor] = tempIDs
  return (histDict)


def jsonDump(dict, writeFile):
  with open(writeFile, 'wb') as fp:
    json.dump(dict, fp)
  print "done writing", writeFile


if __name__=='__main__':
  minCost = 0

  benSumFile = "DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv"
  jsonWriteFile = "costHist.json"

  ptCostList = readBenSum(benSumFile)
  ptHist = makeHistogram(ptCostList)
 
  # print "index\tfloor\tceiling\tlength"
  # for i in sorted(ptHist):
  #   print i, "\t", ptHist[i]["floor"], "\t", ptHist[i]["ceiling"], "\t", ptHist[i]["length"]

  jsonDump(ptHist, jsonWriteFile)