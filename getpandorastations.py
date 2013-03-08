import xml.etree.cElementTree as XML

import requests
import select
import socket
import logging, traceback
import re

response = requests.get('http://feeds.pandora.com/feeds/people/scottscool/stations.xml')

pandora_stations = {}
dom = XML.fromstring(response.content)
for stations in dom.findall(".//item"):
	title = stations.find("title").text
	station_code = stations.find('.//{http://www.pandora.com/rss/1.0/modules/pandora/}stationCode').text
	pandora_stations[title] = station_code.strip("sh")
	#print title
	#print station_code
print pandora_stations
