from machine import Pin, Timer
from dht import DHT22
class mtemperature():
	def __init__(self, ptemperature, phumidity):
		self.ptemperature = ptemperature
		self.phumidity = phumidity
		self.period = 101
		self.counter = 0
		self.dht = DHT22(Pin(4))
	def routine(self):
		if self.counter == 0:
			self.dht.measure()
			self.ptemperature(self.dht.temperature())
			self.phumidity(self.dht.humidity())
		self.counter = (self.counter + 1) % self.period
	def start(self):
		self.counter = 0
		self.routine()
	def stop(self):
		pass
