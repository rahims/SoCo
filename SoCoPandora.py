import xml.etree.cElementTree as XML

import requests
import select
import socket
import logging, traceback
import re
import urllib2
import json
import urllib

email_account = "scottscool@gmail.com"
email_account = urllib.unquote_plus(email_account)
get_user_name = urllib2.Request("http://www.pandora.com/services/ajax/?method=authenticate.emailToWebname&email=" + email_account)
opener = urllib2.build_opener()
user_name_data = opener.open(get_user_name)
json = json.loads(user_name_data.read())
user_name = json['result']['webname']

get_pandora_user_data = requests.get('http://feeds.pandora.com/feeds/people/' + user_name + '/stations.xml')

pandora_stations = {}
pandora_DOM = XML.fromstring(get_pandora_user_data.content)
for stations in pandora_DOM.findall(".//item"):
	title = stations.find("title").text
	station_code = stations.find('.//{http://www.pandora.com/rss/1.0/modules/pandora/}stationCode').text
	pandora_stations[title] = station_code.strip("sh")
return pandora_stations
