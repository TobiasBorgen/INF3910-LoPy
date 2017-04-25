import time
from machine import Pin

count = 0

def pin_handler(arg):
	global count
	count = count + 1
	print(count)

speed = Pin('P12', mode = Pin.IN, pull = Pin.PULL_UP)

speed.callback(Pin.IRQ_FALLING, pin_handler)

while True:
	pass
