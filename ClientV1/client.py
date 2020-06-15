############################################################
# Created on Thursday 21:02:53 2020                        #
#                                                          #
# @author: spraka21@asu.edu                                #
#                                                          #
# Client Program to Drive the Federated Learning Tasks     #
############################################################


import requests
import util
import time
import runFL



header = "http://"
IP = util.getServerIP()
PORT = ":5000"
annouceAPI = header + IP + PORT + "/announce"
submitFLReportAPI = header + IP +PORT + "/submitReport"

################################################################################
# Class to Call Federated Learning Tasks on this Client                        #
# input:                                                                       #
#    clientID : The requesterID specified in the 'client.ini' file             #                                                           #
#    startrow : starting row for the current client specified in config file   #
#    Iterationlen : Iterationlen for the current client specified in config    #
#                   file                                                       #
#    currentTerm : Current Term for the FL task
################################################################################


class FlClient:
    def __init__(self,clientID,startrow,Iterationlen,currentTerm):
        self.clientID = clientID
        self.startrow = startrow
        self.Iterationlen = Iterationlen
        self.currentTerm = currentTerm

    ################################################################################
    # Function to call the announce API of the server to participate in an FL tasks#
    # CallData:                                                                    #
    #    flrequest: A json request made by the client to notify it's availablity   #
    # output:                                                                      #
    #    Receives an FL plan from the server which is an aggregated model          #
    #    parameters for a given FL Iteration                                       #
    ################################################################################
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

    ################################################################################
    # Function to run the FL tasks in the client using Naive Bayes algorithm upon  #
    # reception of an FL tasks from a client                                       #
    # CallParameters:                                                              #
    #    flplan: A json response received by the client from the server            #
    #    startrow : starting row for the current client specified in config file   #
    #    Iterationlen : Iterationlen for the current client specified in config    #
    # output:                                                                      #
    #    Receives an FL Report (model parameter learnt)                            #
    ################################################################################
    def runmodel(self):
        runob = runFL.runfl(self.flplan,self.startrow,self.Iterationlen)
        runob.feature_calculation()
        runob.prediction()
        self.flreport = runob.generate_fl_report()
        self.flreport['currentIteration'] = self.currentTerm
        self.flreport['submitterID'] = self.clientID

    ################################################################################
    # Function to make synchronous call to submitReport API of the server to       #
    # and report the model parameter learnt in the given iteration                 #                                                  #
    # CallData:                                                                    #
    #    FlModelParameters: A json response of model parameters                    #
    # output:                                                                      #
    #    Receives acknowledge from the server                                      #
    ################################################################################
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

################################################################################
# Class to Drive(create an object of Federated Learning Tasks for this client) #
# input:                                                                       #
#    clientID : The requesterID specified in the 'client.ini' file             #                                                           #
#    startrow : starting row for the current client specified in config file   #
#    Iterationlen : Iterationlen for the current client specified in config    #
#                   file                                                       #
#    currentTerm : Current Term for the FL task
################################################################################
class FlClientDriver():
    def __init__(self):
        self.clientID = util.loadUserInfo()
        self.startrow, self.IterationCount, self.Iterationlen = util.InterationInfo()
        #print (self.startrow, self.IterationCount, self.Iterationlen)
        #print ("here")
        self.runFL()

    ################################################################################
    # Function to create object to drive the complete FL tasks for certain number  #
    # of iteration as specified in the config file                                 #
    # CallData:  (all data necessary to create FL tasks object                     #
    #    clientID : The requesterID specified in the 'client.ini' file             #                                                           #
    #    startrow : starting row for the current client specified in config file   #
    #    Iterationlen : Iterationlen for the current client specified in config    #
    ################################################################################
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

