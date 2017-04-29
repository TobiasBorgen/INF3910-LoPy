from config import dev_eui, app_eui, app_key
from lora import LORA
from davis7911 import DAVIS7911
import time
##from si7021 import SI7021

def setup():
  global n, sensor_davis, sensor_temp

  # Connect to LoRaWAN
  n = LORA()
  n.connect(dev_eui, app_eui, app_key)

  # Connect Davis sensor
  try:
    ##sensor_temp = SI7021()
    sensor_davis = DAVIS7911()
  except Exception as e:
    print('Error: ', e)

def format_s(wind_speed):
  windspeedstr = ''
  if wind_speed >= 10:
    windspeedstr = str(wind_speed) + '.00'
  else:
    windspeedstr = '0' + str(wind_speed) + '.00'
  return windspeedstr

def format_d(wind_dir):
  winddirstr = ''
  if wind_dir > 360:
    winddirstr = '360'
  elif wind_dir < 0:
    winddirstr = '0'
  else:
    winddirstr = str(wind_dir)
  return winddirstr

if __name__ == '__main__':
  setup()

  while True:
    
    # Send payload
    speed = format_s(sensor_davis.get_windspeed())
    direction = format_d(sensor_davis.get_dir())
     ##print(direction)
    data = '0' + '018.00' + speed + direction
    response = n.send(data)
    ##hum = sensor_temp.getRH()
    ##temp = sensor_temp.readTemp()
    ##print(temp)
   
    time.sleep(60)  
