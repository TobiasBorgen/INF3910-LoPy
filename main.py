from config import dev_eui, app_eui, app_key
from lora import LORA
from time import sleep
#from davis7911 import DAVIS7911
from packet import Packet
from si7021 import SI7021

def setup():
  global n, sensor_davis, sensor_temp, packet

  # Init packet object
  packet = Packet()

  # Connect to LoRaWAN
  n = LORA()
  n.connect(dev_eui, app_eui, app_key)

  # Connect Sensors
  try:
    sensor_temp = SI7021()
    #sensor_davis = DAVIS7911()
    pass
  except Exception as e:
    print('Error: ', e)

if __name__ == '__main__':

  # Setup network & sensors
  setup()
  max  = 0
  min = 1000000000

  while True:
    
    # Measure
    try:
      packet.set_t(sensor_temp.readTemp())
      packet.set_s(5.23)
      #packet.set_t(sensor_temp.getRH())
      #packet.set_s(sensor_davis.get_windspeed())
      #packet.set_d(sensor_davis.get_dir())
    except Exception as e:
      print('Measure error: ', e)


    # Send packet
    response = n.send(packet.get())
    
    sleep(2)  

