#from flask import Flask , render_template
from retry import retry
import pika
import time
import json
from code_challenge_base_predictor import Predictor
import logging 
import graypy



print("launching sciflask",flush=True)

class ConsumePredictReturn():
	def __init__(self,queue):
		self.my_logger = logging.getLogger('test_logger')
		self.my_logger.setLevel(logging.DEBUG)
		self.handler = graypy.GELFTCPHandler('graylog','12201')
		self.my_logger.addHandler(self.handler)
		self.my_logger.debug("launching sciflask")
		self.queue = queue
		self.Model = Predictor()
		self.my_logger.info("Consume Predict starting...")
		print("",flush=True)
		self.Consume()

	# sends back the probabilities to a new queue probabilities return
	def ReturnSignals(self,inputs, results):
		self.channel.basic_publish(exchange='',
		                      routing_key='probabilities_return',
		                      body=json.dumps(inputs.extend(list(results[0]))))
		self.my_logger.debug("returned prob..{}".format(inputs))

	# on consume, take in data, run through model, return signal, deliver Ack	
	def callback(self,ch,method,properties,body):
		inputs = json.loads(body)
		results = self.Model.predict(json.loads(body))
		self.ReturnSignals(inputs, results)
		self.my_logger.info("Results {}".format(results))
		ch.basic_ack(delivery_tag = method.delivery_tag)
		
	
	# Try Connecting and consuming data from queue,
	#retry handles race condition makes code a tiny bit more robust. 
	@retry(pika.exceptions.AMQPConnectionError, delay=5,jitter=(1,3))
	def Consume(self):
		self.my_logger.info("Attempting to start Consume")
		credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit1',5672,'/',credentials))
		self.channel = self.connection.channel()
		#Data in
		self.channel.queue_declare(queue = self.queue)
		#Probabilities out
		self.channel.queue_declare(queue = 'probabilities_return')
		#Blocks. 
		#print("Consuming Data",flush=True)
		self.channel.basic_consume(queue=self.queue,on_message_callback=self.callback)

		try:
			self.my_logger.info("Consuming")
			self.channel.start_consuming()

		except KeyboardInterrupt:
			self.my_logger.warning("KeyboardInterrupt")
			self.channel.stop_consuming()
			self.connection.close()
		except pika.exceptions.ConnectionClosedByBroker:
			pass

ConsumePredictReturn('queue1')
#ConsumePredictReturn('queue2')