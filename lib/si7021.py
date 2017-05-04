from time import sleep
from machine import I2C

class SI7021(object):
  'Si7021-A20 sensor library for Pycom LoPy'
  
  i2c = None

  # Definitions.
  # https://www.silabs.com/Support%20Documents%2FTechnicalDocs%2FSi7021-A20.pdf
  
  # I2C slave address
  ADDR = 0x40
  
  # Commands, *_HOLD = use of clock line
  HUMD_MEASURE_HOLD = 0xE5
  HUMD_MEASURE_NOHOLD = 0xF5
  TEMP_MEASURE_HOLD = 0xE3
  TEMP_MEASURE_NOHOLD = 0xF3
  TEMP_PREV = 0xE0

  # Heater
  HEATER_REG_ON = 0x3E
  HEATER_REG_OFF = 0x3A

  # User registers
  WRITE_USER_REG = 0xE6
  READ_USER_REG = 0xE7

  # Misc.
  SOFT_RESET = 0xFE
  
  def __init__(self):
    self.i2c = I2C(0, I2C.MASTER)
    
  def measure(self, command):
    # Read only msb and lsb for old temp
    nBytes = 3
    if (command == self.TEMP_PREV):
      nBytes = 2
    
    # Write command to sensor
    self.i2c.writeto(self.ADDR, bytearray([command]))
    # Wait for conversion
    sleep(0.25)
    
    # msb = 0
    # lsb = 1
    recv = self.i2c.readfrom(self.ADDR, 2)
    
    # Clear last bits of lsb to 00
    cleared = recv[1] & 0xFC
    measurement = recv[0] << 8 | cleared
    return measurement
    
  def writeReg(self, value):
    self.i2c.writeto(self.ADDR, bytearray([self.WRITE_USER_REG, value]))
    
  def readReg(self):
    self.i2c.writeto(self.ADDR, bytearray([self.READ_USER_REG]))
    recv = self.i2c.readfrom(self.ADDR, 1)
    return recv
  
  def getRH(self):
    code = self.measure(self.HUMD_MEASURE_HOLD)
    return ((125.0 * code / 65536) - 6)
    
  def getTemp(self):
    code = self.measure(self.TEMP_MEASURE_HOLD)
    return ((175.72 * code / 65536) - 46.85)
    
  # Read temp from previous HD measurement
  def readTemp(self):
    code = self.measure(self.TEMP_PREV)
    return ((175.72 * code / 65536) - 46.85)
    
  def heaterOn(self):
    self.writeReg(self.HEATER_REG_ON)
    
  def heaterOff(self):
    self.writeReg(self.HEATER_REG_OFF)
  
  def reset(self):
    self.writeReg(SOFT_RESET)
