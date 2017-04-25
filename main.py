import time
from machine import Pin

count = 0

def pin_handler(arg):
	global count
	count = count + 1
	##print(count)

speed = Pin('P12', mode = Pin.IN, pull = Pin.PULL_UP)

speed.callback(Pin.IRQ_FALLING, pin_handler)

while True:
	time.sleep(3)
	print("Iterations last 3 seconds", count)

	mph = count * (2.25/3)
	ms = mph * 0.447
	print("Wind speed in m/s", ms)
	count = 0
