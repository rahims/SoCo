

import urllib2
import json
req = urllib2.Request("http://www.pandora.com/services/ajax/?method=authenticate.emailToWebname&email=scottscool%40gmail.com")
opener = urllib2.build_opener()
f = opener.open(req)
json = json.loads(f.read())
print json['result']['webname']