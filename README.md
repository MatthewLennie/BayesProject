# BayesProject
The key features were successfully implemented and work quite well. 
The optional tasks of robustness and logging were somewhat attended to but the result is not as good as I would like. 

SendFile
- Opens the uploaded data
- sends to Rabbit. 

ConsumePredict
- Consumes Rabbit Data
- Provides callback for data event
- returns transformed data into a seperate rabbit queue
- Can switch the source in the initializer at the bottom, not very elegant but the wiring is there. 

Code Challenge...
- opens scikit-learn
-transforms. 

Rabbit
 - Message broker in a prebuilt docker file, not much to comment on. 
 - Management UI port: 15762

 GrayLog
 - Does Logging, Badly.... 
 - Unfortunately, its very slow and you have to manually add the inputs into the web interface. 
 - Instructions here how to pull up the inputs. https://blogs.sap.com/2016/06/29/demo-on-configuring-graylog-input-and-get-messages-2/
 - Currently the Logging system is the mostly likely thing to crash the system rather than record crashes. 
 - interface on -> localhost:9000

Robustness
- python data publishers and consumers run wrapped in retry decorators to handle the race condition at start up. 
- Docker-compose file will restand up the rabbitMQ server incase of outage. 
- No attempt was made to retain state. 


Things that need to be fixed up. 
- Password secret management. 
- The sender module should share connections across send objects in order to avoid repeat opening and closing of the connections to the broker. 
- The gray logging container is horribly slow in the current config, tried to implement the ELK setup instead but wasn't up to stand it up in time.  
- Logging Coverage is currently sparse

Things that I haven't considered:
- Security in general
- Rigorous testing
- Efficient use of computational resources... 
- testing outside of local system. 