import requests
import util
import time
import runFL


header = "http://"
IP = util.getServerIP()
PORT = ":5000"
annouceAPI = header + IP + PORT + "/announce"
submitFLReportAPI = header + IP +PORT + "/submitReport"

class FlClient:
    def __init__(self,clientID,startrow,Iterationlen,currentTerm):
        self.clientID = clientID
        self.startrow = startrow
        self.Iterationlen = Iterationlen
        self.currentTerm = currentTerm

    def announce(self):
        flrequest = util.generateflrequest()
        flrequest['currentIteration'] = self.currentTerm
        #print ("flrequest",flrequest)
        while True:
            response = requests.post(annouceAPI,json=flrequest)
            #print(response)
            if response.status_code == 200:
                print ("FL New Request Submitted Successfully")
                self.flplan = response.json()
                print ("Received FL Plan from server")
                print (self.flplan)
                break
            print("Could not submit FL request\n Retrying after sleep")
            time.sleep(10)

    def runmodel(self):
        runob = runFL.runfl(self.flplan,self.startrow,self.Iterationlen)
        runob.feature_calculation()
        runob.prediction()
        self.flreport = runob.generate_fl_report()
        self.flreport['currentIteration'] = self.currentTerm
        self.flreport['submitterID'] = self.clientID

    def reportresult(self):
        print ("Report for the Current Term ",self.currentTerm)
        print ("Report to be sent to server")
        print (self.flreport)
        while True:
            #print ("I am Busy")
            response = requests.post(submitFLReportAPI, json=self.flreport)
            #print (response)
            if response.status_code == 200:
                print("FL Report Submitted Successfully")
                break
            print ("Could not Submit FL Report\n Retrying After Sleep")
            time.sleep(10)


class FlClientDriver():
    def __init__(self):
        self.clientID = util.loadUserInfo()
        self.startrow, self.IterationCount, self.Iterationlen = util.InterationInfo()
        #print (self.startrow, self.IterationCount, self.Iterationlen)
        #print ("here")
        self.runFL()


    def runFL(self):
        iterationCount = int(self.IterationCount)
        iterationLen = int(self.Iterationlen)
        self.startrow = int(self.startrow)

        for i in range(1,iterationCount+1):
            self.currentTerm = util.currentIteration()
            flobj = FlClient(self.clientID,self.startrow,iterationLen,self.currentTerm)
            flobj.announce()
            flobj.runmodel()
            flobj.reportresult()
            iterationLen += int(self.Iterationlen)
            #print (iterationLen)
            util.updateCurrentTerm(int(self.currentTerm) + 1)


if __name__=="__main__":
    FlClientDriver()

