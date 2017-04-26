import utime
from machine import Pin

class DAVIS7911(object):
  'Davis 7911 sensor library for Pycom LoPy'
  
  timeout = None
  rotations = 0

  # Pins
  pin_windspeed = None
  
  def __init__(self):
    self.timeout = utime.ticks_ms()

    try:
      self.pin_windspeed = Pin('P11', mode = Pin.IN, pull = Pin.PULL_UP)
      self.pin_windspeed.callback(Pin.IRQ_FALLING, self.rotations_handler)
    except Exception as e:
      pass
    
  def rotations_handler(self, arg):
    self.rotations = self.rotations + 1

  def mph_to_ms(self, mph):
    return mph * 0.447

  def get_windspeed(self):
    # Timeout in millis, probably has to be in seconds
    delta_time = (utime.ticks_ms() - self.timeout)/1000
    if(delta_time == 0):
      delta_time = 10

    mph = self.rotations * (2.25 / delta_time)
    self.rotations = 0
    self.timeout = utime.ticks_ms()
    return round(self.mph_to_ms(mph), 0)
