from network import LoRa
import socket
import time
import pycom
import binascii
from machine import Pin

wind_rotations = 0
wait_time = 10

pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x000000) #LED off

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTAA authentication parameters
dev_eui = binascii.unhexlify("00000000000001a0")
app_eui = binascii.unhexlify("0000000000000079")
app_key = binascii.unhexlify("7136523654696d734b64673878484264")

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network
count = 0
while not lora.has_joined():
    pycom.rgbled(0xff0000)
    time.sleep(2.5)
    pycom.rgbled(0x000fff)
    print("Not yet joined count is:" ,  count)
    count = count + 1

print ("After while, count is: ",  count)
# create a LoRa socket
pycom.rgbled(0x0000ff)
time.sleep(0.1)
pycom.rgbled(0x000000)
time.sleep(0.1)
pycom.rgbled(0x0000ff)
time.sleep(0.1)
pycom.rgbled(0x000000)

print("Create LoRaWAN socket")
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket non-blocking
s.setblocking(False)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

def pin_handler(arg):
  global wind_rotations
  wind_rotations = wind_rotations + 1

speed = Pin('P11', mode = Pin.IN, pull = Pin.PULL_UP)
speed.callback(Pin.IRQ_FALLING, pin_handler)

def get_wind_speed():
    global wind_rotations,  wait_time
    rotations = wind_rotations
    print("Iterations last 10 seconds", rotations)
    mph = rotations * (2.25/wait_time)
    ms = mph * 0.447
    print("Wind speed in m/s", ms)
    wind_rotations = 0
    return ms

while True:
    wind_speed = get_wind_speed()
    windspeedstr = ""
    if wind_speed >= 10:
        windspeedstr = str(wind_speed) + ".00"
    else:
        windspeedstr = "0" + str(wind_speed) + ".00"
        
    data = "0" + "005.00" + windspeedstr + "220.00"
    s.send(data)
    print("Sendt:", data)
    pycom.rgbled(0x00ff00)
    time.sleep(0.1)
    pycom.rgbled(0x000000)
    time.sleep(0.1)
    pycom.rgbled(0x00ff00)
    time.sleep(0.1)
    pycom.rgbled(0x000000)
    print("Sending data done...")
    # get any data received...
    response = s.recv(64)
    print("Response:",  response)
    time.sleep(wait_time)
