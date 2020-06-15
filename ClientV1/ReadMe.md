To run client
------------------------------
	Configuration 
	--------------------
	1) Specify the requesterID for the client 
	2) Specify the serverIP for the server
	3) To run this code you need a dataset "mnist.data"
	    a) Since dataset is one and clients could be many
	       Devide the dataset in accordance with the number of clients
	       The range are 0-5000 : for 2 clients startrow for first can be 
	       0 and 2500, similarily for 3 clients startrow can be 0,1500,3000 etc
	    
	    b) Specify the number of iterations to converge the FL Runtime based on number of clients
	    c) Specify how many number of columns is needed in each iteration
	        e:g if 500 is specified for first itertions algorithm runs for 1000 datasets 
	        500 of each label. for 2nd iteration Algorithm runs on 2000 datasets 1000 each label
	        and so on. For 5th iteration it runs on 5000 datasets 2500 for each label
	        
	        With number of clients ensure , the datasets maximum range is not duplicated
	        
	        This is only ment for learning purpose, some biases may occur
	
	Note : The requester ID should be unique for each client    
	
	Install Dependencies
	---------------------
	assuming python 3>0 and pip install in the system
	use command: pip install -r requirements.txt

	Run
	---------------------
	python client.py