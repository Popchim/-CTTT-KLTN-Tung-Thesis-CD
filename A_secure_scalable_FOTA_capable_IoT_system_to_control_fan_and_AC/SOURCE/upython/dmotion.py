from machine import Pin, Timer
from utime import sleep
class mmotion():
	def __init__(self, pmotion):
		self.publish = pmotion
		self.pin = Pin(36, Pin.IN)
		self.holdtimer = Timer(1)
	def setpositive(self, timer=None):
		self.publish(1)
	def setnegative(self, timer=None):
		self.publish(0)
	def edgetrigger(self, pin):
		if pin.value():
			self.holdtimer.deinit()
			self.setpositive()
		else:
			self.holdtimer.init(period=5000, mode=Timer.ONE_SHOT, callback=self.setnegative)
	def routine(self):
		pass
	def start(self):
		self.last = None
		self.pin.irq(handler=self.edgetrigger)
	def stop(self):
		self.pin.irq(None)
