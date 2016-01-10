# What is it?
This is a Plugin for the [XChat IRC client](http://xchat.org) written in Python. It enables a new command `/geoip` that prints the user's location. It also hooks to the `join` event so whenever a user joins a channel, the location of that user is determined and printed. If the user can not be located, a message telling so will be printed.

# Prerequisites
The [MaxMind](https://www.maxmind.com/en/home) GeoIP package and database must be installed on the computer. In addition, the City(Lite) database must be installed. This database can be [downloaded here](http://dev.maxmind.com/geoip/geoip2/geolite2/) for free. The paid / pro version of the City database works as well, of course. 

# IPv6
IPv6 addresses are not understood. However, the script could be easily  adapted to lookup IPv6 addresses as well. The MaxMind IPv6 database is relatively small as of today (Jan 2016) and therefore implementing this at this point in time is not very useful.

# Installing
The script should be copied into the `~/.xchat2` directory. To load the script, use 

	/py load geoip-lookup.py
	
To reload / or unload replace `load` with `reload` or `unload`, respectively.

# Using
Use `/geoip <username>` in the server context as you'd use `/whois`. In fact, using `/whois` produces also a location line when the plugin is loaded. In a channel window, the `/geoip <username>` prints the same same line as if the user just joined. The latter use is useful for users that are already in the channel and where a lookup is desired.

#Links and Pages
* [XChat Python Plugin](http://xchat.org/docs/xchatpython.html)
* [GeoIP / MaxMind Python Binding documentation](https://github.com/maxmind/geoip-api-python/blob/master/examples/country.py)
* [XChat scripting documentation](http://xchatdata.net/Scripting)
* [XChat Text Formatting](http://xchatdata.net/Scripting/TextFormatting)