from config import dev_eui, app_eui, app_key
from lora import LORA
from davis7911 import DAVIS7911
from packet import Packet
from si7021 import SI7021
from time import sleep
from machine import deepsleep
import ujson


def setup():
  global n, sensor_davis, sensor_temp, packet, sleep_time, state

  # Initial state and sleeptime
  state = 7
  sleep_time = 10
  
  # Init packet object
  packet = Packet()

  # Connect to LoRaWAN
  n = LORA()
  n.connect(dev_eui, app_eui, app_key)

  # Connect Sensors
  try:
    sensor_temp = SI7021()
    sensor_davis = DAVIS7911()
  except Exception as e:
    print('Error: ', e)

def handle_response(data):
  global sleep_time, state

  try:
    response = ujson.loads(data)[0]
  except ValueError as e:
    print("Exception occured while parsing response",  e)
    return
  try:
    state = int(response['f'])
  except:
    print("No new format to set")
  try:
    sleep_time = int(response['u'])
  except:
    print("No new update interval")

if __name__ == '__main__':

  # Setup network & sensors
  setup()

  while True:
    sleep(sleep_time) # 10s
    # Measure
    try:
      #packet.set_t(sensor_temp.getRH()) 
      if(state == 7 or state == 6 or state == 5 or state == 4):
        packet.set_t(sensor_temp.getTemp())
      if(state == 7 or state == 6 or state == 3 or state == 2):
        packet.set_s(sensor_davis.get_windspeed())
      if(state == 7 or state == 5 or state == 3 or state == 1):
        packet.set_d(sensor_davis.get_dir())
    except Exception as e:
      print('Measure error: ', e)


    # Send packet
    response = n.send(packet.get())
    if (len(response) > 0):
        handle_response(response)

    
    #deepsleep(10000) # 10s

