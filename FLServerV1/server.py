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
