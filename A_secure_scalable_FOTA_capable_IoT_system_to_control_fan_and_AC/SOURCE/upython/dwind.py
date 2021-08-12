from machine import Pin, Timer
class mwind():
	def __init__(self):
		self.value = None
		self.period = 1
		self.pin = Pin(32, Pin.IN)
		self.filled = 0
		self.accum = 0
	def edgetrigger(self, pin=None):
		self.filled = 1
	def routine(self):
		if self.filled:
		        self.accum += 1
		else:
		        self.accum = 0
		if self.accum >= 140:
		        self.value = 1
		        self.accum = 140
		else:
		        self.value = 0
		self.filled = 0
	def start(self):
		self.value = 0
		self.filled = 0
		self.accum = 0
		self.pin.irq(handler=self.edgetrigger)
	def stop(self):
		self.pin.irq(None)
