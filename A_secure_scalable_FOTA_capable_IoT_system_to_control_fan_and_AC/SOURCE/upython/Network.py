import utime
import network
def do_connect(password, ssid):    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    for i in ssid:
      if not wlan.isconnected():
          wlan.connect(i, password)
          utime.sleep(3)
      if wlan.isconnected():
          break
    result = wlan.isconnected()
    if result:
        print('network config:', wlan.ifconfig())       
    else:
        print('no wlan available')
    return result
