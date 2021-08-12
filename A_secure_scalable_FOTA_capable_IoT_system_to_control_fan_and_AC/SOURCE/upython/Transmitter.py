from esp32 import RMT
from machine import Pin
class Transmitter():
	def __init__(self, channel, freq=38000, duty=33, x=26):
		self.rmt = RMT(channel, pin=Pin(x), clock_div=80, carrier_freq=freq, carrier_duty_percent=duty)
	def on(self, bi, choice=2):
		leading = [[9000, 4500], [3418, 3418], [3471, 3471]]
		normal = [[[563, 562], [563, 1687]], [[872, 871], [872, 2614]], [[868, 868], [868, 2593]]]
		stop = [562, 872, 868]
		code = []
		if (choice < 2):
			code = leading[choice]
			for i in bi:
				if i == '0':
					code += normal[choice][0]
				elif i == '1':
					code += normal[choice][1]
		elif (choice == 2):
			for i in range(len(bi)):
				if (i % 32 == 0):
					code += leading[choice]
				if (bi[i] == '0'):
					code += normal[choice][0]
				elif (bi[i] == '1'):
					code += normal[choice][1]
		code += [stop[choice]]
		self.rmt.write_pulses(code, start=1)
