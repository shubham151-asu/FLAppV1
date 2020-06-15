# FLAppV1
 Federated Learning is a type of distributed Machine Learning in which the
 ML algorithms runs on the edge devices or clients and model parameters are 
 send to the server instead of data. Server receives the model parameters 
 and performs aggregation and sends back aggregated model to the clients. 
 There are multiple possible implementation of federated learning such as
 Horizontal Learning, Vertical Learning or Transfer learning. The implemented 
 algorithm uses Horizontal learning in way (without using SGD). It uses a 
 simple ML algorithm like Naive Bayes because of the property of conditional
 independence among the features. The features learnt from different clients
 can be aggregated and the aggregated model parameters can be sent back to the 
 clients for classification. As the model learns the aggregated model converges 
 and classification accuracy achieved is as good as learnt from a single system.
 

To run server
------------------------------
	Configuration 
	--------------------
	Specify the number of clients (or systems ) that are particpating in the FL tasks in 'server.ini' file
	Suppose system count is 2.
	clientCount : 2

	Install Dependencies
	---------------------
	assuming python 3>0 and pip install in the system
	use command: pip install -r requirements.txt

	Run
	---------------------
	python server.py


To run the gracefully First start the server and then start all clients 