from machine import Pin, Timer
from esp32 import RMT
from dwind import mwind
class mfan():
	def __init__(self, pfanready, pfanbusy, pstate):
		self.ready = pfanready
		self.pbusy = pfanbusy
		self.publish = pstate
		self.iwind = mwind()
		self.desired = None
		self.busy = None
		self.period = 29
		self.counter = 0
		self.latest = None
		self.inittime = 340
		self.first = 1
		self.holdtimer = Timer(2)
		self.rmt = RMT(0, pin=Pin(23), clock_div=80, carrier_freq=38000, carrier_duty_percent=33)
		self.busy = 0
		self.code = {}
		self.code['leading']	= [3418, 3418]
		self.code['0']		= [872, 871] 
		self.code['1']		= [872, 2614]
		self.code['stop']	= [872]
		self.code['command']	= '110111000001001000111110'
	def setdesiredstate(self, desired):
		self.desired = desired
	def updatestate(self):
		if self.iwind.value > 0:
			if self.latest != 1:
				self.latest = 1
				self.publish(1)
		else:
			if self.latest != 0:
				self.latest = 0
				self.publish(0)
	def resolve(self, timer=None):
		self.busy = 0
		self.pbusy(0)
	def toggle(self):
		buf = []
		buf += self.code['leading']
		command = self.code['command']
		logic0 = self.code['0']
		logic1 = self.code['1']
		for i in command:
			if i == '0':
			        buf += logic0
			elif i == '1':
			        buf += logic1
		buf += self.code['stop']  
		self.rmt.write_pulses(buf, start=1)
	def routine(self, timer=None):
		self.iwind.routine()
		if self.inittime > 0:
			self.inittime -= 1
		else:
			if self.counter == 0:
				if not self.busy:
					if self.first:
						self.first = 0
						self.ready()
						print('Ready')
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
		self.iwind.start()
		self.inittime = 350
		self.counter = 0
		self.busy = 0
		self.first = 1
		self.latest = None
		self.routine()
	def stop(self):
		self.iwind.stop()
