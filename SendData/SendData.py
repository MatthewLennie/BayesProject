import pika
from retry import retry
import time 
import csv
import json
import logging
import graypy



class SendDataObj():
	def __init__(self,FileName,queue):
		self.my_logger = logging.getLogger('test_logger')
		self.my_logger.setLevel(logging.DEBUG)
		self.handler = graypy.GELFTCPHandler('graylog','12201')
		self.my_logger.addHandler(self.handler)
		self.my_logger.info("launching SendData")

		self.FileName = FileName	
		self.queue = queue
		self.SendData()

		

	#Loads up data from CSV	
	def GrabData(self):
		with open(self.FileName) as csvfile:
			contents = csv.reader(csvfile)
			next(contents,None)
			data = []
			for row in contents:	
				data.append([float(x) for x in row[1:]])
			#print(data)
		return data

	#Opens up server connection. uses retry to handle race condition
	@retry(pika.exceptions.AMQPConnectionError, delay=5,jitter=(1,3))
	def SendData(self):
		credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
		connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit1',5672,
		                                       '/',
		                                       credentials))
		channel = connection.channel()
		channel.queue_declare(queue=self.queue)
		#Load data from disk
		file_contents = self.GrabData()
		#Try sending it. 
		try:
			for row in file_contents:
				channel.basic_publish(exchange='',
					                      routing_key=self.queue,
					                      body=json.dumps(row))
				self.my_logger.debug("Sent from {}".format(self.queue))
				
			connection.close()

		except KeyboardInterrupt:
			self.my_logger.warning("KeyboardInterrupt")
			if connection: 
				connection.close()
		except pika.exceptions.ConnectionClosedByBroker:
			pass


#Just send data syncronously 
SendDataObj('code_challenge_data1.csv','queue1')
SendDataObj('code_challenge_data2.csv','queue2')