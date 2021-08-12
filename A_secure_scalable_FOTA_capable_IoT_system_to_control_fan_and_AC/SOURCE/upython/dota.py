from machine import Pin
from Ota import *
from Credential import REPO, TOKEN 
class mota():
	def __init__(self):
		self.led = Pin(2, Pin.OUT)
		self.ota = OTAUpdater(REPO, headers={'Authorization': 'token {}'.format(TOKEN)})
	def checkupdate(self):
		self.ota.check_update()
	def getversion(self):
		return self.ota.get_version(self.ota.modulepath(self.ota.main_dir))
	def installupdate(self):
		self.led.on()	
		res = self.ota.install_update()
		self.led.off()
		return res
	def update(self):
		self.led.on()	
		res = self.ota.check_and_install_update()
		self.led.off()
		return res
