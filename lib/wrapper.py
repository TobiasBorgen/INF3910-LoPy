import pycom
import time

class LED(object):
    'Wrapper class for controlling the LED'
    
    def heartbeat(state):
        pycom.heartbeat(state)
        
    def on():
        pycom.rgbled(0x00FF00)

    def off():
        pycom.rgbled(0x000000)
        
    def blink(n = 0, d = 0.5, c = 0x0000ff):
        """
        Blink the LED.
        n = number of times to blink
        d = duration of the light
        c = color
        """
        for x in range(n):
            pycom.rgbled(0x000000)
            time.sleep(d)
            pycom.rgbled(c)
            time.sleep(0.1)
