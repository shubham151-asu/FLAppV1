import json
import os
from configparser import ConfigParser
from threading import Thread,Lock
import glob
import numpy as np

lock = Lock()
config = ConfigParser()
config.read('server.ini')


fldata =  {
            'features': {
                'meanofmean7': [0,0],
                'meanofmean8': [0,0],
                'covariance7': [[0,0],[0,0]],
                'covariance8': [[0,0],[0,0]],
                'count7': 0,
                'count8': 0,
            },
            'accuracy': 0,
            'currentIteration': 0,
            'submitterID':0,
        }


flplan = 'FLplan'
iteration = "Iterations"
flreport = 'FlReport'

def init_flplan():
    if not os.path.isdir(flplan):
        os.makedirs(flplan)
    if not os.path.isdir(iteration):
        os.makedirs(iteration)
    if not os.path.isdir(flreport):
        os.makedirs(flreport)
    filepath = flplan + '/flmodel0.txt'
    file = open(filepath,'w')
    json.dump(fldata,file)
    file.close()

def getrawplan():
    return fldata.copy()

def getclientcount():
    return int(config['clientsInfo']['clientCount'])


def waitandcheck(destDir):
    clientCount = getclientcount()
    while True:
        #print ("I keep server busy ")
        lock.acquire()
        filecount = len(glob.glob(destDir + "\\*.txt"))
        lock.release()
        if filecount == clientCount:
            break
    return filecount


################################################################################
# Function to aggregate model parameters received from all clients             #
################################################################################
def aggregate(destDir, filecount, iteration):
    count7 = 0
    count8 = 0
    meanofmean7 = np.zeros(2,float)
    meanofmean8 = np.zeros(2,float)
    covariance7 = np.array([[0.0, 0.0], [0.0, 0.0]])
    covariance8 = np.array([[0.0, 0.0], [0.0, 0.0]])
    accuracy = 0
    for i in range(1,filecount+1):
        file = destDir + "/flReport" + str(i) + ".txt"
        with open(file,"r") as openfile:
            jsondata = json.load(openfile)
        openfile.close()
        features = jsondata["features"]
        count7 += features['count7']
        count8 += features['count8']
        meanofmean7 += np.array(features['meanofmean7']) / filecount
        meanofmean8 += np.array(features['meanofmean8']) / filecount
        covariance7 += np.array(features['covariance7']) / filecount
        covariance8 += np.array(features['covariance8']) / filecount
        accuracy += jsondata["accuracy"]
        #print (count7,count8)
    fldata = getrawplan()
    fldata['features']['count7'] = count7
    fldata['features']['count8'] = count8
    fldata['features']['meanofmean7'] = meanofmean7.tolist()
    fldata['features']['meanofmean8'] = meanofmean8.tolist()
    fldata['features']['covariance7'] = covariance7.tolist()
    fldata['features']['covariance8'] = covariance8.tolist()
    fldata['accuracy'] = accuracy / filecount
    fldata['currentIteration'] = iteration
    requestfilepath = flplan +"/flmodel" + str(iteration) + ".txt"
    with open(requestfilepath, "w") as openfile:
        json.dump(fldata, openfile)
    openfile.close()


################################################################################
# Function to make the calls synchronous by polling and waiting until all the  #
# clients have sent an FL request or FL report in a given iteration            #
################################################################################
def startPoll(destDir,iteration):
    filecount = waitandcheck(destDir)
    while True:
        lock.acquire()
        requestfilepath = flplan + "/flmodel" + str(iteration) +  ".txt"
        check =  os.path.isfile(requestfilepath)
        if not check:
            aggregate(destDir,filecount,iteration)
            lock.release()
            break
        else:
            lock.release()
            break