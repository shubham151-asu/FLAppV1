############################################################
# Created on Thursday 21:02:53 2020                        #
#                                                          #
# @author: spraka21@asu.edu                                #
#                                                          #
# Server Program to aggregate data from clients for a      #
# Federated Learning Tasks                                 #
############################################################


from flask import Flask, request, jsonify
import os
import json
import util


app = Flask(__name__)

util.init_flplan()



def returnflplan(iteration):
    lastIteration = str(int(iteration) - 1)
    destFile =  "Flplan/flmodel" + lastIteration + ".txt"
    responseFlplan = json.load(open(destFile))
    return responseFlplan

################################################################################
# Function to server as endpoint for the announce API synchronous call made by #
# the clients, until all the client request are made no response are sent      #
# ReceiveData:                                                                    #
#    flrequest: A json request made by the client to notify it's availablity   #
# Action:                                                                      #
#    Sends an FL plan to the client which is an aggregated model parameters    #
#    from the previous FL Iteration                                            #
################################################################################
@app.route("/announce", methods=['POST'])
def announce():
    message = request.get_json()
    iteration = message['currentIteration']
    requesterID = message['requesterID']
    destDir = "Iterations/Iteration" + str(iteration)
    requestfilepath = destDir + "/Requester" + requesterID + ".txt"
    if not os.path.isdir(destDir):
        os.makedirs(destDir)
    with open(requestfilepath,"w") as requestfile:
        requestfile.write("RequestNoticed from requester %s"%(requesterID))
    requestfile.close()
    util.waitandcheck(destDir)
    return jsonify(returnflplan(iteration))


################################################################################
# Function to server as endpoint for the announce API synchronous call made by #
# the clients, until all the client request are made no response are sent      #
# ReceiveData:                                                                 #
#    flReport: A json report send by the client about the model parameters it  #
#               has learnt in the given iteration                              #
# Action:                                                                      #
#    Aggregates the FL model parameters received from all clients              #
################################################################################

@app.route("/submitReport", methods=['POST'])
def reportflmodel():
    message = request.get_json()
    iteration = message['currentIteration']
    requesterID = message['submitterID']
    destDir = "FLReport/Iteration" + str(iteration)
    requestfilepath = destDir + "/flReport" + requesterID +".txt"
    #print ("Reached Server")
    if not os.path.isdir(destDir):
        os.makedirs(destDir)
    with open(requestfilepath,"w") as requestfile:
        json.dump(message,requestfile)
    requestfile.close()
    util.startPoll(destDir,iteration)
    return jsonify(success = 'Thanks for submitting Results of Iteration %s'%(iteration))



if __name__ == "__main__":
    app.run(debug='True',host="0.0.0.0")
