import lora
import socket
import time
import binascii
import pycom
import uos
from config import dev_eui, app_eui, app_key

# Connect to LoRaWAN
n = lora.LORA()
n.connect(dev_eui, app_eui, app_key)

## Will give a random number between start and end, works within 0-99, may perform bad for small numbers
def rand_uniform(start, end):
    while True:
        bnum = uos.urandom(2)
        num = int(bnum[0]) + int(bnum[1])
        if((num > start) and (num < end)):
            return num

pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x000000) #LED off

# create a LoRa socket
pycom.rgbled(0x0000ff)
time.sleep(0.1)
pycom.rgbled(0x000000)
time.sleep(0.1)
pycom.rgbled(0x0000ff)
time.sleep(0.1)
pycom.rgbled(0x000000)

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
    response = n.send(data)
    pycom.rgbled(0x00ff00)
    time.sleep(0.1)
    pycom.rgbled(0x000000)
    time.sleep(0.1)
    pycom.rgbled(0x00ff00)
    time.sleep(0.1)
    pycom.rgbled(0x000000)
    print("Sending data done...")
    # get any data received...
    print("Response:",  response)
    time.sleep(30)
