#from flask import Flask , render_template
from retry import retry
import pika
import time
import json
from code_challenge_base_predictor import Predictor
import logging 
import graypy

my_logger = logging.getLogger('test_logger')
my_logger.setLevel(logging.DEBUG)
handler = graypy.GELFTCPHandler('graylog','12201')
my_logger.addHandler(handler)
my_logger.debug("hello")

print("launching sciflask",flush=True)

class ConsumePredictReturn():
	def __init__(self,queue):

		self.queue = queue
		self.Model = Predictor()
		print("Consume Predict starting...",flush=True)
		self.Consume()

	# sends back the probabilities to a new queue probabilities return
	def ReturnSignals(self,inputs, results):
		self.channel.basic_publish(exchange='',
		                      routing_key='probabilities_return',
		                      body=json.dumps(inputs.extend(list(results[0]))))
		print("returned prob..{}".format(inputs))

	# on consume, take in data, run through model, return signal, deliver Ack	
	def callback(self,ch,method,properties,body):
		inputs = json.loads(body)
		results = self.Model.predict(json.loads(body))
		self.ReturnSignals(inputs, results)
		ch.basic_ack(delivery_tag = method.delivery_tag)
		
	
	# Try Connecting and consuming data from queue,
	#retry handles race condition makes code a tiny bit more robust. 
	@retry(pika.exceptions.AMQPConnectionError, delay=5,jitter=(1,3))
	def Consume(self):
		credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit1',5672,'/',credentials))
		self.channel = self.connection.channel()
		#Data in
		self.channel.queue_declare(queue = self.queue)
		#Probabilities out
		self.channel.queue_declare(queue = 'probabilities_return')
		#Blocks. 
		print("Consuming Data",flush=True)
		self.channel.basic_consume(queue=self.queue,on_message_callback=self.callback)

		try:
			self.channel.start_consuming()
		except KeyboardInterrupt:
			self.channel.stop_consuming()
			self.connection.close()
		except pika.exceptions.ConnectionClosedByBroker:
			pass

for i in range(10000):
	time.sleep(10)
	my_logger.debug("hello")
	my_logger.warning("hadsfasd")
	print("sending debugs",flush=True)

ConsumePredictReturn('queue1')


#app = Flask(__name__)
	#
	#@app.route('/')
	#def home():
	#	return render_template('template.html',my_string=log)
	#

	#app.run(debug=True,host='0.0.0.0')