import time
import si7021

sensor = si7021.SI7021()

count = 0
while True:
  try:
    hum = sensor.getRH()
    temp = sensor.readTemp()

    if (count == 2):
      sensor.heaterOn()
      print("Turning heater ON")

    if (count == 12):
      sensor.heaterOff()
      print("Turning heater OFF")

    print("TEMP: ", temp, ", HUM: ", hum)

  except OSError as e:
    print("Exception occured while measuring data")
    print("errno: ", e.errno)

  count = count + 1
  time.sleep(10)
