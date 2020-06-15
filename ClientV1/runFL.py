############################################################
# Created on Sunday 21:02:53 2020                        #
#                                                          #
# @author: spraka21@asu.edu                                #
#                                                          #
# Client Program to Drive the Federated Learning Tasks     #
############################################################

import sys
import scipy.io
import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal

################################################################################
# Class to run a Federated Learning Tasks on this Client                       #
# input:                                                                       #
#    clientID : The requesterID specified in the 'client.ini' file             #                                                           #
#    startrow : starting row for the current client specified in config file   #
#    Iterationlen : Iterationlen for the current client specified in config    #
#                   file                                                       #
################################################################################

class runfl:
    def __init__(self,flplan,startrow,iterationlen):
        if not flplan:
            print('No FLPLAN')
            sys.exit()
        self.load_flplan(flplan,startrow,iterationlen)
        self.numpyfile = scipy.io.loadmat("mnist_data.mat")

    ################################################################################
    # Function to load FL Plan from server after announcement received             #
    ################################################################################
    def load_flplan(self,flplan,startrow,iterationlen):
        self.fliterationlen = iterationlen
        self.startrow = startrow
        self.features = flplan['features']
        self.currentTerm = int(flplan['currentIteration'])

    ################################################################################
    # Function to return a dummy FL report                                         #
    ################################################################################
    def get_new_flpan(self):
        fldata_ds = {
            'features': {
                'meanofmean7': [0, 0],
                'meanofmean8': [0, 0],
                'covariance7': [[0, 0], [0, 0]],
                'covariance8': [[0, 0], [0, 0]],
                'count7': 0,
                'count8': 0,
            },
            'accuracy': 0,
            'currentIteration': 0,
            'submitterID': 0,
        }
        return fldata_ds

    ################################################################################
    # Function to generate FL report after the model has learnt                    #
    ################################################################################
    def generate_fl_report(self):
        response_fl_report = self.get_new_flpan()
        response_fl_report['features']['count7'] = self.count7
        response_fl_report['features']['count8'] = self.count8
        response_fl_report['features']['meanofmean7'] = self.meanofmean7.tolist()
        response_fl_report['features']['meanofmean8'] = self.meanofmean8.tolist()
        response_fl_report['features']['covariance7'] = self.covariance7.tolist()
        response_fl_report['features']['covariance8'] = self.covariance8.tolist()
        response_fl_report['accuracy'] = self.accuracy
        #response_fl_report['submitterID'] = self.submitterID
        return response_fl_report

    ################################################################################
    # Function to pre-processes to aggregate label data for the MNIST dataset      #
    ################################################################################
    def preprocessing(self):
        print ('PreProcessing started')
        tsrows = self.numpyfile['tsX'].shape[0]
        # tsrows = 50
        self.train_X = pd.DataFrame(columns=["Mean", "std"])
        self.train_Y = pd.DataFrame(columns=['labels'])
        self.test_X = pd.DataFrame(columns=["Mean", "std"])
        train_Y = self.numpyfile['trY']

        self.test_Y = self.numpyfile['tsY']
        #print (self.train_X.shape,self.train_Y.shape)
        #print(self.numpyfile['trY'][0][6264], self.numpyfile['trY'][0][6266])
        count = 0
        for row in range(self.startrow, self.startrow + self.fliterationlen):
            mean = np.mean(self.numpyfile['trX'][row])
            std = np.std(self.numpyfile['trX'][row])
            frame = {"Mean": mean, "std": std}
            self.train_X.loc[count] = frame
            self.train_Y.loc[count] = {'labels':0}
            count += 1

        for row in range(self.startrow, self.startrow + self.fliterationlen):
            mean = np.mean(self.numpyfile['trX'][row+6265])
            std = np.std(self.numpyfile['trX'][row+6265])
            frame = {"Mean": mean, "std": std}
            self.train_X.loc[count] = frame
            self.train_Y.loc[count] = {'labels': 1}
            count +=  1

        self.totalcount = count

        for row in range(0, tsrows):
            mean = np.mean(self.numpyfile['tsX'][row])
            std = np.std(self.numpyfile['tsX'][row])
            frame = {"Mean": mean, "std": std}
            self.test_X.loc[row] = frame
        #print (self.train_X)
        #print (self.train_Y)
        print('PreProcessing done')

    ################################################################################
    # Function to learn model parameter from the aggregated labels                 #
    ################################################################################
    def feature_calculation(self):
        self.preprocessing()
        print ('Feature Calculation start')
        count7 = 0
        count8 = 0
        trx_7 = pd.DataFrame(columns = ["Mean","std"])
        trx_8 =  pd.DataFrame(columns = ["Mean","std"])
        #print (self.train_Y.loc[0].values)
        for col in range(0,self.totalcount):
            if self.train_Y.loc[col].values==0:
                trx_7.loc[count7] = self.train_X.loc[col]
                count7 +=1
            else:
                trx_8.loc[count8] = self.train_X.loc[col]
                count8 +=1

        #print (trx_7)
        #print (trx_8)
        self.count7 = count7
        self.count8 = count8
        self.prob7 = self.count7 / (self.count7 + self.count8)
        self.prob8 =  self.count8 / (self.count7 + self.count8)
        self.meanofmean7 = trx_7.mean().values
        self.meanofmean8 = trx_8.mean().values
        self.covariance7 = trx_7.cov().values
        self.covariance8 = trx_8.cov().values
        print('Feature Calculation done')

    ################################################################################
    # Function to make prediction from the model parameters learnt from client data#
    # in a given iteration                                                         #
    ################################################################################
    def prediction(self):
        print('Prediction process Started from Client Data')
        tsrows = self.numpyfile['tsX'].shape[0]
        #tsrows = 50
        test_count7 = 0
        test_count8 = 0
        accurate_count = 0
        for row in range(0, tsrows):
            feature = self.test_X.loc[row]
            prob_7 = multivariate_normal.logpdf(feature, mean=self.meanofmean7, cov=self.covariance7) + np.log(
                self.prob7)
            prob_8 = multivariate_normal.logpdf(feature, mean=self.meanofmean8, cov=self.covariance8) + np.log(
                self.prob8)

            verification = 0 if prob_7 > prob_8 else 1
            if self.test_Y[0][row] == 0 and verification == 0:
                test_count7 += 1
            if self.test_Y[0][row] == 1 and verification == 1:
                test_count8 += 1
            if verification ==  self.test_Y[0][row]:
                accurate_count += 1
        self.accuracy = accurate_count / tsrows
        print ("Precidiction accuracy from client Data",self.accuracy)
        print ('Prediction process Done')
        if self.currentTerm>1:
            self.predictionforserver()
        return self.generate_fl_report()


    ################################################################################
    # Function to make prediction from the aggregated model parameters learnt from #
    # server in a given iteration                                                  #
    ################################################################################
    def predictionforserver(self):
        print('Prediction process Started from Server Data')
        tsrows = self.numpyfile['tsX'].shape[0]
        #tsrows = 50
        test_count7 = 0
        test_count8 = 0
        accurate_count = 0
        meanofmean7 = self.features['meanofmean7']
        meanofmean8 = self.features['meanofmean8']
        covariance7 = self.features['covariance7']
        covariance8 = self.features['covariance8']
        count7 = self.features['count7']
        count8 = self.features['count8']
        prob7 = count7 / (count7 + count8 + 0.000001)
        prob8 = count8 / (count7 + count8 + 0.000001)
        for row in range(0, tsrows):
            feature = self.test_X.loc[row]
            prob_7 = multivariate_normal.logpdf(feature, mean=meanofmean7, cov=covariance7) + np.log(
                prob7)
            prob_8 = multivariate_normal.logpdf(feature, mean=meanofmean8, cov=covariance8) + np.log(
                prob8)

            verification = 0 if prob_7 > prob_8 else 1
            if self.test_Y[0][row] == 0 and verification == 0:
                test_count7 += 1
            if self.test_Y[0][row] == 1 and verification == 1:
                test_count8 += 1
            if verification ==  self.test_Y[0][row]:
                accurate_count += 1
        self.accuracy = accurate_count / tsrows
        print ("Precidiction accuracy from server Data",self.accuracy)
        print('Prediction process Done')
        return


# flplan = {
#             'features': {
#                 'meanofmean7': [0,0],
#                 'meanofmean8': [0,0],
#                 'covariance7': [[0,0],[0,0]],
#                 'covariance8': [[0,0],[0,0]],
#                 'count7': 0,
#                 'count8': 0,
#             },
#             'accuracy': 0,
#             'curIteration': 0,
#             'submitterID': 0,
#         }

# newobj = runfl(flplan,2500,1000)
# newobj.feature_calculation()
# flresponse = newobj.prediction()
# print (flresponse)