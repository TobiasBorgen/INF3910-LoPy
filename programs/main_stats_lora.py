import os
import time
import utime
import ujson
import binascii
import machine
import lora
from config import dev_eui, app_eui, app_key
import si7021

# Connect to LoRaWAN
n = lora.LORA()
n.connect(dev_eui, app_eui, app_key)

# Connect sensor
sensor = si7021.SI7021()

def send_payload(data):
    hum = 0
    temp = 0
    
    # Hum & temp
    try:
        hum = sensor.getRH()
        temp = sensor.readTemp()
    except OSError as e:
        print("Exception occured while measuring data")
        print("errno: ", e.errno)
        
    final = {
        'resource_hum': hum,
        'resource_temp': temp,
        'resource_data': ujson.dumps(data)
    }
    n.send(ujson.dumps(final))
    time.sleep(10)

count = 0
while True:
    print("Cycle ", count)
    count = count + 1
    
    # Platform
    data = os.uname()
    send_payload({
        'sysname':      data[0],
        'nodename':     data[1],
        'release':      data[2],
        'version':      data[3],
        'machine':      data[4]
    })
    
    # RTC
    send_payload({'rtc': utime.time()})
    
    # Sysclk
    send_payload({'sysclk': machine.freq()})
    
    # Device ID
    send_payload({'device_id': binascii.hexlify(machine.unique_id())})
    
    # LoRa bandwidth
    send_payload({'bandwidth': n.lora.bandwidth()})
    
    # LoRa frequency
    send_payload({'frequency': n.lora.frequency()})
    
    # LoRa power mode
    send_payload({'power_mode': n.lora.power_mode()})
    
    # LoRa MAC
    send_payload({'mac': n.lora.mac()})
