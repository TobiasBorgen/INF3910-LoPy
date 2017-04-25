from config import dev_eui, app_eui, app_key
from lora import LORA
from davis7911 import DAVIS7911
import time

def setup():
  global n, sensor_davis

  # Connect to LoRaWAN
  n = LORA()
  n.connect(dev_eui, app_eui, app_key)

  # Connect Davis sensor
  sensor_davis = DAVIS7911()

def format(wind_speed):
  windspeedstr = ''
  if wind_speed >= 10:
    windspeedstr = str(wind_speed) + '.00'
  else:
    windspeedstr = '0' + str(wind_speed) + '.00'
  return '0' + '005.00' + windspeedstr + '220.00'

if __name__ == '__main__':
  setup()

  while True:
    # Send payload
    data = format(sensor_davis.get_windspeed())
    response = n.send(data)

    time.sleep(10)
