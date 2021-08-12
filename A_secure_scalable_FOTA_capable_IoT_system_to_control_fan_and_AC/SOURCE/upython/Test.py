from Transmitter import *
from Remote import *
from utime import sleep_ms
def test_duty(remote, channel, dt, rep):
	print('Checking accurary for duty ' + str(dt))
	t = Transmitter(channel, duty=dt)
	for i in range(rep):
		t.on('00000000111111111010001001011101')
		sleep_ms(500)
	return remote.report()
def test_duties(remote, start, rep):
	l = [test_duty(remote, i, start + i, rep) for i in range(8)]
	accuracy = max(l)
	best = start + l.index(accuracy)
	print("Best duty: ", best)
	print("Best duty accuracy: ", accuracy)
	return best
class Tester():
	def __init__(self):
		self.r = Remote()
		self.r.on()
	def test(self, start, rep=20):
		return test_duties(self.r, start, rep)
