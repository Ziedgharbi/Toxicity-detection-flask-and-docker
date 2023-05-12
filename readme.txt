Descreption : 

	- This application is for prediction comment classe's 
	- There are 7 classes : toxicity, severe_toxicity, obscene, threat, insult, identity_attack, sexual_explicit 


How to create docker image :

	- Open cmd 
	- Go to project directory 
	- Excute command  docker build -t name_image .
	- Run docker image by : docker run -p 5000:5000 name_image:tag

	
For app testing, please use the json file which can be loaded from : "https://dummyjson.com/comments" 