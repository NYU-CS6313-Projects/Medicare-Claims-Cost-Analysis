import csv
import json

def readFile(file):
  
  with open(file, "rb") as csvfile:
    xWalk = csv.reader(csvfile)
    headers = xWalk.next()
    
    xWalkDict = {}
    for line in xWalk:
      dxCode = line[0].strip("'").strip(" ")
      xWalkDict[dxCode] = {}
      xWalkDict[dxCode]["l1code"]   = line[1].strip("'")
      xWalkDict[dxCode]["l1label"]  = line[2].strip("'").upper()
      xWalkDict[dxCode]["l2code"]   = line[3].strip("'")
      xWalkDict[dxCode]["l2label"]  = line[4].strip("'").upper()
      xWalkDict[dxCode]["l3code"]   = line[5].strip("'")
      xWalkDict[dxCode]["l3label"]  = line[6].strip("'").upper()
      xWalkDict[dxCode]["l4code"]   = line[7].strip("'")
      xWalkDict[dxCode]["l4label"]  = line[8].strip("'").upper()

    return(xWalkDict)

def jsonDump(dict, writeFile):
  with open(writeFile, 'wb') as fp:
    json.dump(dict, fp)
  print "done writing", writeFile

if __name__=='__main__':
  xWalkFile = "ccs_multi_dx_tool_2015.csv"
  writeFile = "diagnosisXwalk.json"
  xWalkDict = readFile(xWalkFile)
  jsonDump(xWalkDict, writeFile)