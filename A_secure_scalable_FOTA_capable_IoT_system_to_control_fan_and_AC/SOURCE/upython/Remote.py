from utime import ticks_us, ticks_diff
from machine import Timer, Pin

class Remote():

	def __init__(self, x=23, choice=1):
		self.buf = [0 for x in range(1000)]
		self.last = 0
		self.pin = Pin(x, Pin.IN, Pin.PULL_UP)
		self.i = 0
		self.now = 0
		self.timer = Timer(1)
		self.unit = [1125, 1743]
		self.roof = [3000, 4000]
		self.choice = choice
		self.mul = 1.7
		#self.logs = ['']*100
		#self.lind = 0
		self.leadings = []
		self.lows = []
		self.highs = []
		#self.stoppings = []
		#self.avgs = [0.0]*100
		#self.ind = 0
		#self.savgs = []

	def collect(self, p):
		self.now = ticks_us()
		if (self.last != 0):
			self.buf[self.i] = ticks_diff(self.now, self.last)
			self.i += 1
		self.last = self.now
	
	def process(self, t):
		if ticks_diff(ticks_us(),self.last) > 120000 and self.i > 2:
			print('-------------------------------------------------------------')
			#self.logs[self.lind] = self.decode()
			#res = self.decode()
			#print("HEX: ", "{0:#0{1}x}".format(int(self.logs[self.lind], 2),10))
			#print("HEX: ", "{0:#0{1}x}".format(int(res, 2),10))
			#print("BIN: ", self.logs[self.lind])
			print("CODE: ", self.buf[:400])
			#self.savgs += list(filter(lambda x: x >= 30000 and x < 40000, self.buf))
			#self.avgs[self.ind] = 0.5 * (self.buf[0]+self.buf[1])
			self.summarize()
			self.last = 0
			self.i = 0
			for x in range(len(self.buf)):
        			self.buf[x] = 0
			#self.lind += 1
			#self.ind += 1
	
	def on(self):
		#self.pin.irq(self.collect, Pin.IRQ_RISING|Pin.IRQ_FALLING)
		self.pin.irq(self.collect, Pin.IRQ_RISING|Pin.IRQ_FALLING)
		self.timer.init(mode=Timer.PERIODIC, period=100, callback=self.process)
	
	def off(self):
		self.timer.deinit()
		self.pin.irq(None)
	
	def decode(self):
		code = ''
		for j in range(1,self.i):
			if self.buf[j] < self.unit[self.choice]*self.mul:
				code += '0'
			elif self.buf[j] < self.roof[self.choice]:
				code += '1'
		if code == '':
			code = '0'
		return code
	
#	def report(self):
#		score = 0
#		for i in self.logs[:self.lind]:
#			if (i == '00000000111111111010001001011101'):
#				score += 1
#		percent = score/self.lind
#		self.lind = 0
#		print('Accuracy: ', percent)
#		return percent
		
#	def stats(self):
#		tmp = self.avgs[:self.ind]
#		avg = sum(tmp)/len(tmp)
#		print('Average of leading pulses: ', avg)
#		self.ind = 0
#	 	savg = sum(self.savgs)/len(self.savgs)
#		print('Average of stop pulses:', savg)
#		self.savgs = []
#		return (avg, savg)

	def summarize(self):
		los = list(filter(lambda x: x < 2000 and x > 100, self.buf))
		his = list(filter(lambda x: x >= 2000 and x < 3000, self.buf))
		leads = list(filter(lambda x: x >= 3000 and x < 4000, self.buf))
		self.leadings.append(sum(leads)/len(leads))
		self.lows.append(sum(los)/len(los))
		self.highs.append(sum(his)/len(his))
	
	def stats(self):
		leading = sum(self.leadings)/len(self.leadings)
		low = sum(self.lows)/len(self.lows)
		high = sum(self.highs)/len(self.highs)
		print('Leading pulse average: ', leading)
		print('Low pulse average: ', low)
		print('High pulse average: ', high)
		self.leadings = []
		self.lows = []
		self.highs = []
