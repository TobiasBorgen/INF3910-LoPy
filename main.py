from network import LoRa
import socket
import time
import binascii
import pycom
import uos

## Will give a random number between start and end, works within 0-99, may perform bad for small numbers
def rand_uniform(start, end):
    while True:
        bnum = uos.urandom(2)
        num = int(bnum[0]) + int(bnum[1])
        if((num > start) and (num < end)):
            return num

pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x000000) #LED off

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)


# create an OTAA authentication parameters
dev_eui = binascii.unhexlify("0000000000000178")
app_eui = binascii.unhexlify("0000000000000079")
app_key = binascii.unhexlify("6258336f4f7038665445473943326436")

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

# create a LoRa socket
pycom.rgbled(0x0000ff)
time.sleep(0.1)
pycom.rgbled(0x000000)
time.sleep(0.1)
pycom.rgbled(0x0000ff)
time.sleep(0.1)
pycom.rgbled(0x000000)

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket non-blocking
s.setblocking(False)

print ("After while, count is: ",  count)

print("Create LoRaWAN socket")

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)

count = 0

## Starting values ##
temp = 20
speed = 10
direction = 210

while True:

    ## Randomly increase or decrease variables by up to five ##
    if int(uos.urandom(1)[0]) > 5:
        temp += int(rand_uniform(0,5))
    else:
        temp -= int(rand_uniform(0,5))

    if int(uos.urandom(1)[0]) > 5:
        speed += int(rand_uniform(0,5))
    else:
        speed -= int(rand_uniform(0,5))

    if int(uos.urandom(1)[0]) > 5:
        direction += int(rand_uniform(0,5))
    else:
        direction -= int(rand_uniform(0,5))

    if temp < -50 or temp > 80:
        temp = 20
    if speed < 0 or speed > 80:
        speed = 10
    if direction < 0 or direction > 360:
        direction = 210


    ## Create string variables for easier string manipulation ##
    tempstr = str(temp)
    speedstr = str(speed)
    dirstr = str(direction)

    ## Modify temperature string ##
    if int(temp) < 10:
        tempstr = "0" + tempstr
    if temp < 0:
        tempstr = "0" + tempstr + "." + str(rand_uniform(0,99))
    else:
        tempstr = "0" + tempstr + "." + str(rand_uniform(0,99))

    ##Modify speed string ##
    if speed < 10:
        speedstr = "0" + speedstr + "." + str(rand_uniform(0,99))
    else:
        speedstr = speedstr + "." + str(rand_uniform(0,99))

    ## Modify direction string ##
    if direction < 100:
        dirstr = "0" + dirstr + "." + str(rand_uniform(0,99))
    else:
        dirstr = dirstr + "." + str(rand_uniform(0,99))

    ## Send payload with 0 for all sensors enabled ##
    print("Send data: " +  tempstr + " Celsius, " + speedstr + " m/s, " + dirstr +" degrees batch_nr: ")
    data = "0" + tempstr + speedstr + dirstr
    print(data)

    count = count + 1
    # send some data
    s.send(data)
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
    time.sleep(30)
