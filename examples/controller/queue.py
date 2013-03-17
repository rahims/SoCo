
import sys
import time
import ui_out


from soco import SoCo
from zone import SoHome
from preset import Service

class Queue( Service):

    queue_name = "Sonos Queue"

    def __init__(self, a_speaker):
		self.current = 0
		self.stations.append( { 'title':self.queue_name })
		
    def play_current_preset(self, the_sonos):
#      result = the_sonos.play_uri( uri, metadata)
      result = True
      return result
	  
      

