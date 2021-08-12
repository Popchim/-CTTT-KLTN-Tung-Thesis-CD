from Mqtt import *
import gc
from machine import Timer, unique_id
from utime import sleep
from binascii import hexlify
from Credential import SERVER, PASSPHRASE 
class mmqtt():
	def __init__(self, system):

		self.system = system
		self.setdesiredfanstate = None
		self.setdesiredairconstate = None

		#self.timer = Timer(230)
		self.period = 23
		self.counter = 0 
		self.connected = 0

		self.id = hexlify(unique_id()).decode('ascii')
		self.server = SERVER
		self.timeout = 10
		self.clean = 1
		self.ssl = True

		self.user = 'esp32'
		self.password = PASSPHRASE

		self.lwtopic = 'Connection/' + self.id
		self.lwmsg = 'esp32 disconnected'
		self.lwretain = False
		self.lwqos = 1
		
		self.make()	

	def make(self):
		CERT_REQUIRED = 0xffffff
		from Credential import CA
		self.client = MQTTClient(self.id, self.server, user=self.user, password=self.password, keepalive=self.timeout, ssl=self.ssl, ssl_params={'cert_reqs':CERT_REQUIRED, 'ca_certs':CA})
		del CA	
		self.setlastwill()
		self.setcallback()
	def setlastwill(self):
		self.client.set_last_will(self.lwtopic, self.lwmsg, self.lwretain, self.lwqos)	
	def setcallback(self):
		self.client.set_callback(self.process)	
	def connect(self):
		gc.collect()
		self.client.connect(clean_session=self.clean)
		gc.collect()
	def publish(self, topic, msg='', retain=False, qos=1):
		self.client.publish(topic, msg, retain, qos)
	def process(self, topic, msg):
		print('Topic: ', topic)
		print('Message: ', msg)
		if topic == b'Fan-control/'+self.id:
			try:
				self.setdesiredfanstate(int(msg))
			except:
				pass
		elif topic == b'Aircon-control/'+self.id:
			try:
				self.setdesiredairconstate(int(msg))
			except:
				pass
		elif topic == b'Ota-control':
			if msg == b'1':
				self.system.update()
		elif topic == b'Reset-control/'+self.id:
			if msg == b'1':
				self.system.reset()
	def subscribe(self, topic, qos=1):
		self.client.subscribe(topic, qos)
	def waitmsg(self):
		return self.client.wait_msg()
	def checkmsg(self):
		return self.client.check_msg()
	def pdeath(self):
		self.publish(self.lwtopic, self.lwmsg)
	def disconnect(self):
		self.pdeath()
		self.client.disconnect()
	def ping(self):
		self.client.ping()
	def close(self):
		self.client.close()
	def pid(self):
		self.publish('ID', self.id)
	def pversion(self):
		self.publish('Version/' + self.id, self.system.getversion())
	def ptemperature(self, temperature):
		self.publish('Temperature/' + self.id, str(temperature))
	def phumidity(self, humidity):
		self.publish('Humidity/' + self.id, str(humidity))
	def plighting(self, lighting):
		self.publish('Lighting/' + self.id, str(lighting))
	def pmotion(self, motion):
		self.publish('Motion/' + self.id, str(motion))
	def pfan(self, fan):
		self.publish('Fan/' + self.id, str(fan))
	def paircon(self, aircon):
		self.publish('Aircon/' + self.id, str(aircon))
	def pfanready(self):
		self.publish('Fan-ready/' + self.id, '1')
	def pairconready(self):
		self.publish('Aircon-ready/' + self.id, '1')
	def pfanbusy(self, value):
		self.publish('Fan-busy/' + self.id, str(value))
	def pairconbusy(self, value):
		self.publish('Aircon-busy/' + self.id, str(value))
	def routine(self, timer=None):
		if self.counter == 0:
			try:
				self.ping()
				self.checkmsg()
				self.checkmsg()
				self.checkmsg()
				self.counter = (self.counter + 1) % self.period
			except:
				if self.connected:	
					self.connected = 0
					self.system.unconnected()
	def start(self):
		self.counter = 0
		self.connect()
		self.pid()
		sleep(3)
		self.pversion()
		self.subscribe('Fan-control/' + self.id)
		self.subscribe('Aircon-control/' + self.id)
		self.subscribe('Ota-control')
		self.subscribe('Reset-control/' + self.id)
		self.connected = 1
	def stop(self):
		try:
			self.disconnect()
		except:
			self.close()
		finally:
			self.connected = 0
