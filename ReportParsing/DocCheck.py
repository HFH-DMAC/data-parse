#  imports
from dataclasses import dataclass
from datetime import datetime
import os
import csv

#  code starts here
#=======================
#===================
#   DATACLASSES
#===================
@dataclass
class NumberReqs:
    minValue: float
    maxValue: float
    numberType: str # defines if integer, real number, float etc

@dataclass
class ColumnAttributes:
    expectedIndex: int #what column number we expect this data to be in
    reqDataType: str  #for us to define either text or numerical or datetime
    maxLength: int
    illegalCharacters: list[str]
    otherTags: list[str]
    nullAllowed: bool
    colNumberReqs: NumberReqs

@dataclass
class DocumentAttributes:
    fileName: str
    dateUpload: datetime
    submissionRules: list[ColumnAttributes]

#=======================
#===================
#   PRESET VARS
#===================
fileconnectPath = "examplecsvs"
filerulePath = "documentrules.csv"
filesToCheck = []
fileruleset = []

#=======================
#===================
#   FUNCTIONS
#===================

#checking type
def checkMain(ruleobj: ColumnAttributes, checkvalue):
    datatype = ruleobj.reqDataType.strip()

    if (datatype == "text"):
        try:
            return CheckDataLength(ruleobj.maxLength, len(checkvalue))
        except:
            pass

    if (datatype == "number"):
        # since they all read as strings, we have to use an original way to check some properties. Here I utilize the thrown error to check number type
        try:
            int(checkvalue)
            float(checkvalue)
            return True
        except:
            print("failed check number")
            return False
        
    if (datatype == "datetime"):
        try:
            datetime.strptime(checkvalue, "%m/%d/%Y")
            return True
        except:
            print("failed check datetime")
            return False
    else:
        return False

#checking length
def CheckDataLength(maxl, checkl):
    if (maxl > checkl):
        return True
    else:
        return False

def rowCheck(inputrow, rownumber: int):
    #  this will check datatype and print maybe for now
    for cindex, item in enumerate(inputrow, start=0):
        try:
            print(fileruleset[cindex].reqDataType)
            checkresult = checkMain(fileruleset[cindex], item)
            print(checkresult)
        except IndexError:
            pass

#=======================
#===================
#   MAIN SCRIPT
#===================
# get csv files in path, only get the csv files and nothing else
for afilename in os.listdir(fileconnectPath):
    if afilename.endswith(".csv"):
        filesToCheck.append(afilename)
print("Files and directories in '", fileconnectPath, "' :") 
# prints all files
print(filesToCheck)

#  populate the ruleset
with open (filerulePath, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for index, row in enumerate(csvreader, start=0):
        if (index != 0):
            try:
                columnRules = ColumnAttributes(int(row[1]), row[2], int(row[3]), [], [], row[6], NumberReqs(0,0,"none"))
            except ValueError:
                columnRules = ColumnAttributes(int(row[1]), row[2], 100, [], [], row[6], NumberReqs(0,0,"none"))
            except:
                print("some issue")
            
            if (row[2] == 'number'):
                columnRules.colNumberReqs = NumberReqs(float(row[7]), float(row[8]), row[9])

            fileruleset.append(columnRules)
        else:
            pass
#test ruleset
print(len(fileruleset))

#   Now working with individual files in the file array
for afile in filesToCheck:
    with open ((fileconnectPath + "//" + afile), newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for rindex, row in enumerate(csvreader, start=0):
            print(row)
            if (rindex != 0):
                #  send row to another function to check vs the ruleset
                rowCheck(row, rindex)


#=======================
#===================
#   END
#===================
print("done")
elfin = input()