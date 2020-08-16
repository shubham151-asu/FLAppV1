Distributed Machine Learning

In Distributed Machine learning, ML algorithms run on different or isolated Machines.
Based on the performance and learning requirements, datasets availability(distributed or centralized),
few of the use cases can be written as:-

- Case1: Multiple ML algorithms run on different systems using datasets which is available in one storage server. 
       This approach can also be used in ensemble learning.
- Case2: One machine learning algorithm runs on a subset of data on different systems and the model generated can be aggregated. 
       Such algorithms can large datasets

For every use case, there is a need for system design that solves the bottleneck of R/O operations from the storage server 
at the same time and does not compromise with high performance. An extended version of Case2 is Federated learning
where ML algorithms run on the edge devices or clients and model or model parameters are sent to the server instead
of data. The master server receives the model parameters and performs aggregation and sends back the aggregated model 
to the clients. There are multiple possible implementations of federated learning task such as Horizontal Learning, 
Vertical Learning or Transfer learning. 

In this code, the implemented algorithm uses Horizontal learning in a way (without using SGD used in deep learning). 
It uses a Naive Bayes because of the property of conditional independence among the features.The features learned
from different clients can be aggregated and the aggregated model parameters can be sent back to theclients for
classification. As the model learns the aggregated model converges and classification accuracy achieved is as good as 
learning from a single system.
 

To run server
------------------------------
	Configuration 
	--------------------
	Specify the number of clients (or systems ) that are particpating in the FL tasks in 'server.ini' file
	Suppose system count is 2.
	clientCount : 2

	Install Dependencies
	---------------------
	Assuming python 3>=0 and pip already installed in the system
	use command: pip install -r requirements.txt

	Run
	---------------------
	master server : python server.py
	clients : python client.py (data set for the client can be found at https://drive.google.com/drive/folders/1un2aI_8X9tzYhzlT8na0SQteVetfJSDm?usp=sharing



To run the program gracefully, first start the server and then start all clients 
