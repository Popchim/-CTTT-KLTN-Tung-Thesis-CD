from machine import Pin, Timer
class mlighting():
	def __init__(self, plighting):
		self.publish = plighting
		self.period = 19
		self.counter = 0
		self.last = None
		self.pin = Pin(18, Pin.IN)
	def routine(self):
		if self.counter == 0:
			current = 1 - self.pin.value()
			if current != self.last:
				self.last = current
				self.publish(current)
		self.counter = (self.counter + 1) % self.period
	def start(self):
		self.counter = 0
		self.last = None
		self.routine()
	def stop(self):
		pass
