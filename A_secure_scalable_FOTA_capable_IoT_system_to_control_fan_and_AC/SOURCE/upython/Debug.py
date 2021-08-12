from Credential import DEBUG, SSID, PASSWORD, REPO, TOKEN
if DEBUG:
	from Credential import SSID, PASSWORD, REPO, TOKEN
	from network import WLAN, STA_IF
	wlan = WLAN(STA_IF)
	wlan.active(1)
	wlan.connect(SSID, PASSWORD)
	import uasyncio as aio
	from machine import *
	from utime import sleep_ms
	from dregister import *
	from dtemperature import *
	from dlighting import *
	from dmotion import *
	from daircon import *
	from dwind import *
	from dfan import *
	from dmqtt import *
	from dchip import *
	from dota import *
	from dtop import *
	from Http import HttpClient
	http = HttpClient(headers={'Authorization': 'token {}'.format(TOKEN)})
