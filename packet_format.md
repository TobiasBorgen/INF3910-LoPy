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
If included, always 5 bytes.

E.g. -10.2
	
### S `Speed`
If included, always 4 bytes.

E.g. 04.5 (m/s)
	
### D `Direction`
If included, always 3 bytes.

E.g. 145 (degrees)

### Max packet size: 13b
E.g. 0-10.204.5145

All sensors included, -1.15°C, 3.5 m/s, 145 degrees

### Min packet size: 4b

E.g. 1145

Only wind direction included, 145 degrees
