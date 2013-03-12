#!/usr/bin/env python

import sys
import os
import time
import ui_out

import xml.etree.cElementTree as XML
from threading import Thread
import Queue


from preset import Service
import urllib2

class TuneIn( Service):
	
    meta_template =  '&lt;DIDL-Lite xmlns:dc=&quot;http://purl.org/dc/elements/1.1/&quot; xmlns:upnp=&quot;urn:schemas-upnp-org:metadata-1-0/upnp/&quot; xmlns:r=&quot;urn:schemas-rinconnetworks-com:metadata-1-0/&quot; xmlns=&quot;urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/&quot;&gt;&lt;item id=&quot;R:0/0/0&quot; parentID=&quot;R:0/0&quot; restricted=&quot;true&quot;&gt;&lt;dc:title&gt;{title}&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=&quot;cdudn&quot; nameSpace=&quot;urn:schemas-rinconnetworks-com:metadata-1-0/&quot;&gt;{service}&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;'
    tunein_service = 'SA_RINCON65031_'
    info_url =       "http://opml.radiotime.com/Describe.ashx?id=%s&detail=&partnerId=Sonos&serial=%s"
	
    def load_icons(self): 
      while True:
        data = self.queue.get()
        self.process_station_info(data['index'], data[ 'uid'], data['url'])
        self.queue.task_done()
 
    #----------------------------------------------------------------------
    def process_station_info(self, idx, uid, url):
      print 'processing ' + url
      try:
        handle = urllib2.urlopen( url)
        filename = os.path.join( self.path, uid) + '.xml'
        chunk = handle.read()
          
        dom = XML.fromstring(chunk.encode('utf-8'))
        d = dom.findtext('.//logo')
        #TODO there is a whole lot of other good stuff in this file as well
        # e.g. the proper name for the station
        print d
        name, extension = os.path.splitext(d)
      
        filename = os.path.join( self.icons.get_directory(), str(idx)) + extension
        print filename
        f = urllib2.urlopen( d)
        data = f.read()
        with open(filename, "wb") as img:
          img.write(data)
      except:
		print 'oh that went wrong'  
	

    def __init__(self, a_speaker, icon_path, force_update=False):
      super(TuneIn,self).__init__( icon_path)
      self.path = icon_path
      self.queue =  Queue.Queue()
      thread = Thread(target=self.load_icons)
      thread.daemon = True
      thread.start()
      self.get_station_list(a_speaker)
            

	
    def get_metadata( self):
	  return self.meta_template.format(title='', service=self.tunein_service)
		  
		  
    def get_station_list(self, a_speaker):
      gulp = a_speaker.get_favorite_radio_stations( 0, 12)
      print 'returned %s of a possible %s radio stations:' % (gulp['returned'], gulp['total'])
      self.stations = gulp['favorites']	
      
      # get icon images
      mac = a_speaker.get_speaker_info()['serial_number']
      idx=0
      for favorite in self.stations:
        if not self.icons.get_unique_icon( idx):
          id = favorite['uri'].split('?')[0].split(':')[1]
          self.queue.put( {'index':idx, 'uid':id, 'url':self.info_url% (id,mac)} )
        idx=idx+1

if __name__ == '__main__':
   from zone import SoGroup 	
   the_group = SoGroup()
   the_group.modify_zone(['Living Room'])
   ti = TuneIn( the_group.master, 'tunein')
   raw_input('-->')



