from machine import UART
from network import WLAN
import os

wlan = WLAN()
wlan.deinit()

uart = UART(0, 115200)
os.dupterm(uart)
