import lora
import time
import uos
from config import dev_eui, app_eui, app_key

# Connect to LoRaWAN
n = lora.LORA()
n.connect(dev_eui, app_eui, app_key)

# Will give a random number between start and end,
# works within 0-99, may perform bad for small numbers.
def rand_uniform(start, end):
    while True:
        bnum = uos.urandom(2)
        num = int(bnum[0]) + int(bnum[1])
        if((num > start) and (num < end)):
            return num

# Starting values
count = 0
temp = 20
speed = 10
direction = 210

while True:

    # Randomly increase or decrease variables by up to five
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

    # Create string variables for easier string manipulation
    tempstr = str(temp)
    speedstr = str(speed)
    dirstr = str(direction)

    # Modify temperature string
    if int(temp) < 10:
        tempstr = "0" + tempstr
    if temp < 0:
        tempstr = "0" + tempstr + "." + str(rand_uniform(0,99))
    else:
        tempstr = "0" + tempstr + "." + str(rand_uniform(0,99))

    # Modify speed string
    if speed < 10:
        speedstr = "0" + speedstr + "." + str(rand_uniform(0,99))
    else:
        speedstr = speedstr + "." + str(rand_uniform(0,99))

    # Modify direction string
    if direction < 100:
        dirstr = "0" + dirstr + "." + str(rand_uniform(0,99))
    else:
        dirstr = dirstr + "." + str(rand_uniform(0,99))

    data = "0" + tempstr + speedstr + dirstr
    print("Send data: " +  tempstr + " Celsius, " + speedstr + " m/s, " + dirstr +" degrees batch_nr: ")
    print(data)

    # Send payload with 0 for all sensors enabled
    response = n.send(data)
    print("Response:",  response)
    
    count = count + 1
    time.sleep(30)
