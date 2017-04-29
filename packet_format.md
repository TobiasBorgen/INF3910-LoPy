# Packet format

### FTTTTTTSSSSSDDDDDD

### F `Packet format`
Possible values:

* 0 - all sensors excluded
* 1 - only wind direction
* 2 - only wind speed
* 3 - temperature excluded
* 4 - only temperature
* 5 - wind speed excluded
* 6 - wind direction excluded
* 7 - all sensors included
	
### T `Temperature`
If included, always 6 bytes.

E.g. -10.22
	
### S `Speed`
If included, always 5 bytes.

E.g. 04.50 (m/s)
	
### D `Direction`
If included, always 6 bytes.

E.g. 145.87 (degrees)

### Max packet size: 18b
E.g. 0-01.1503.05015.00

All sensors included, -1.15°C, 3.05 m/s, 15 degrees

### Min packet size: 6b

E.g. 505.15

Only wind speed included, 5.15 (m/s)
