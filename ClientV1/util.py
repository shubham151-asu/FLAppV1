from configparser import ConfigParser
import copy
import os

flrequest = {
    "requesterID":0,
    "currentIteration":0
}

configInfo = ConfigParser()
configInfo.read('client.ini')

def currentIteration():
    file = "Iteration.txt"
    if not os.path.isfile(file):
        with open(file,"w") as file:
            file.write(str(1) + "\n")
        file.close()
        return 1
    file = open(file,"r")
    lines = file.readlines()
    file.close()
    currentTerm = lines[-1].split("\n")[0]
    return currentTerm

def updateCurrentTerm(currentTerm):
    filename = "Iteration.txt"
    file = open(filename, "a")
    file.write(str(currentTerm) + "\n")
    file.close()

def loadUserInfo():
    #print (configInfo)
    return configInfo['userdetails']['requesterID']

def getServerIP():
    return configInfo['serverdetails']['serverIP']

def InterationInfo():
    return configInfo['DBInfo']['startRow'],configInfo['DBInfo']['Iterations'],configInfo['DBInfo']['Iterationlen']


def generateflrequest():
    newrequest = flrequest.copy()
    newrequest["requesterID"] = configInfo['userdetails']['requesterID']
    return newrequest

