from machine import Pin, Timer
from esp32 import RMT
class maircon():
	def __init__(self, pairconready, pairconbusy, pstate):
		self.ready = pairconready
		self.pbusy = pairconbusy
		self.publish = pstate
		self.period = 31
		self.counter = 0
		self.first = 1
		self.latest = None
		self.busy = None
		self.holdtimer = Timer(3)
		self.doorstate = Pin(21, Pin.IN, pull=Pin.PULL_UP)
		self.rmt = RMT(1, pin=Pin(27), clock_div=80, carrier_freq=38000, carrier_duty_percent=33)
		self.busy = 0
		self.code = {}
		self.code['leading']	= [3471, 3471]
		self.code['0']		= [868, 868]
		self.code['1']		= [868, 2593]
		self.code['stop']	= [868]
		self.code['command']	= '10000100100001000110000001100000100001001000010001100000011000000000010100000101011011000110110000000101000001010110110001101100'
		self.code['len']	= 128
	def setdesiredstate(self, desired):
		self.desired = desired
	def updatestate(self):
		sample = self.doorstate.value()
		if sample != self.latest:
			self.latest = sample
			self.publish(sample)
	def resolve(self, timer=None):
		self.busy = 0
		self.pbusy(0)
	def toggle(self):
		buf = []
		command = self.code['command']
		logic0 = self.code['0']
		logic1 = self.code['1']
		for i in range(self.code['len']):
			if (i % 32 == 0):
			        buf += self.code['leading']
			if (command[i] == '0'):
			        buf += logic0
			elif (command[i] == '1'):
			        buf += logic1
		buf += self.code['stop']  
		self.rmt.write_pulses(buf, start=1)
	def routine(self):
		if self.counter == 0:
			if not self.busy:
				if self.first:
					self.first = 0
					self.ready()
					self.updatestate()
					self.desired = self.latest
				else:
					self.updatestate()
					if self.latest != self.desired:
						self.busy = 1
						self.pbusy(1)
						self.toggle()
						self.holdtimer.init(period=7000, mode=Timer.ONE_SHOT, callback=self.resolve)
		self.counter = (self.counter + 1) % self.period
	def start(self):
		self.counter = 0
		self.busy = 0
		self.first = 1
		self.latest = None
		self.routine()
	def stop(self):
		pass
