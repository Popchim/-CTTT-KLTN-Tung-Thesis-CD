from machine import reset
from network import WLAN, STA_IF
from utime import sleep
from dota import mota
from dchip import mchip
from Credential import SSID, PASSWORD
class mtop():
	def __init__(self):
		self.wlan = WLAN(STA_IF)
		self.iota = mota()
		self.ichip = mchip(self.wlan, self.iota)
	def start(self):
		self.wlan.active(1)
		self.wlan.connect(SSID, PASSWORD)
		while not self.wlan.isconnected():
			pass
		if self.iota.update():
			reset()
		self.ichip.start()
	def stop(self):
		self.ichip.stop()
