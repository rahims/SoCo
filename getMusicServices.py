import xml.etree.cElementTree as XML

import requests, select, socket
import logging, traceback, re

response = requests.get('http://192.168.1.59:1400/status/securesettings')

dom = XML.fromstring(response.content)
music_login = dom.findtext('.//Command')
music_login =  XML.fromstring(music_login).attrib['Value']

services_login_list = music_login.split(',')
#should put this in a dictionary instead
music_service_credentials = [(services_login_list+[services_login_list[0]])[i:i+4] for i in range(0, len(services_login_list), 4)]

search = '3'
for sublist in music_service_credentials:
    if sublist[0] == search:
        return sublist[1]
        break
