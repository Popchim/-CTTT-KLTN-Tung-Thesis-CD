from machine		import reset, Timer
from network		import WLAN, STA_IF
from utime 		import sleep, sleep_ms
from Obj 		import obj
from dota		import mota
from dtemperature 	import mtemperature
from dlighting 		import mlighting
from dmotion 		import mmotion
from daircon 		import maircon
from dfan 		import mfan
from dmqtt 		import mmqtt
class mchip():
	def __init__(self, wlan, iota):
		self.wlan 				= wlan
		self.iota 				= iota
		self.timer				= Timer(0)
		self.system				= obj()
		self.first				= 0

		self.system.reset			= self.reset
		self.system.unconnected			= self.unconnected
		self.system.update			= iota.update
		self.system.getversion			= iota.getversion

		self.imqtt				= mmqtt		(self.system)

		temperature				= self.imqtt.ptemperature
		humidity				= self.imqtt.phumidity
		lighting				= self.imqtt.plighting
		motion					= self.imqtt.pmotion
		fanready				= self.imqtt.pfanready	
		fanbusy					= self.imqtt.pfanbusy	
		fan					= self.imqtt.pfan
		airconready				= self.imqtt.pairconready	
		airconbusy				= self.imqtt.pairconbusy
		aircon					= self.imqtt.paircon
		
		self.itemperature 			= mtemperature	(temperature, humidity)
		self.ilighting 				= mlighting	(lighting)
		self.imotion 				= mmotion	(motion)
		self.ifan				= mfan		(fanready, fanbusy, fan)
		self.iaircon				= maircon	(airconready, airconbusy, aircon)
		
		self.imqtt.setdesiredfanstate		= self.ifan.setdesiredstate
		self.imqtt.setdesiredairconstate	= self.iaircon.setdesiredstate
	def reset(self):
		reset()
	def unconnected(self):
		self.stop()
		while not self.wlan.isconnected():
			sleep(5)
		self.start()
	def routine(self, timer=None):
		self.itemperature	.routine()
		self.ilighting		.routine()
		self.imotion		.routine()
		self.ifan		.routine()
		self.iaircon		.routine()
	def start(self):
		if self.first:
			self.first = 0
			sleep(50)
		try:
			self.imqtt		.start()
			self.ifan		.start()
			self.iaircon		.start()	
			self.itemperature	.start()
			self.ilighting		.start()
			self.imotion		.start()
			self.timer.init(period=20, mode=Timer.PERIODIC, callback=self.routine)
		except:
			self.unconnected()
	def stop(self):
		self.timer.deinit()
		self.imotion		.stop()
		self.ilighting		.stop()
		self.itemperature	.stop()
		self.iaircon		.stop()
		self.ifan		.stop()
		self.imqtt		.stop()
