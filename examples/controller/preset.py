#!/usr/bin/env python

import threading
import ui_out
from preset_icon import Preset_Icon




class Presets(object):
    """ A container class for preset groups.
    """ 



    def __init__(self, a_sonos):
      self.the_sonos = a_sonos
      print 'controller is ' + str(self.the_sonos)
      self.the_sonos = None
      self.groups = []
      self.current = 0

    def __len__(self): 
      len = 0
      for group in self.groups:
         len = len + len(group)
      return len 

    def add_preset_group( self, a_group):
#      print 'adding ' + str( a_group) + ' ' + str(a_group.current)
      self.groups.append( a_group)
      

    def get_preset(self):
      try:
        url = self.groups[ self.current].get_uri()
        meta = self.groups[ self.current].get_metadata()
        name = self.groups[ self.current].name()
        icon = self.groups[ self.current].icon()
        return {'url':url, 'meta':meta, 'name':name, 'icon':icon}
      except IndexError:
		ui_out.log.error('absolute preset oor')
		return None

    def goto(self, index):
      try:
        self.groups[ self.current].current = index
      except IndexError:
		ui_out.log.error('absolute preset oor')
    	
    def _goto( self, index):
      index = abs(index % len(self))
      for idx, group in self.groups:
        if index < group.len():
          self.current = idx
          self.groups[ self.current].current = index
          return
        else:
		  index = index -  group.len()
        
    	
    		
    def play( self, the_sonos, index=-1):
      self.the_sonos = the_sonos
      try:
        if index != -1:
          self.groups[ self.current].current = index
        self.groups[ self.current].play( self.the_sonos, index)
      except IndexError:
		ui_out.log.error('absolute preset oor')


    def skip( self, direction):
      if len( self.groups) == 0:
        self.current = 0
        ui_out.log.error('no next/pre preset')
        return False
#      print self.current
#     print 'skip ' + str(direction)
      try:
        print 'controller is ' + str(self.the_sonos)
        return self.groups[ self.current].skip( self.the_sonos, direction)
      except IndexError:
        if direction > 0:
#          print 'fault+'
          self.current = self.current + direction
          if self.current == len( self.groups): 
            self.current = 0
          self.groups[ self.current].first()
          return self.groups[ self.current].play( self.the_sonos)
        if direction < 0:
#          print 'fault-'
          self.current = self.current + direction
          if self.current < 0: 
            self.current = len( self.groups) - 1
          self.groups[ self.current].last()
          return self.groups[ self.current].play( self.the_sonos)




class Service(object):
    current = 0
    stations = []
    icons = None
     
                
    def __init__(self, icons_path):
      print 'init'
      self.icons = Preset_Icon( icons_path)
      self.stations = []
      self.current = 0

    def __len__(self): 
      return len(self.stations) 

    def get_uri( self):
      station = self.stations[ int(self.current)]
      uri = station['uri']
      # TODO seems at least & needs to be escaped - should move this to play_uri and maybe escape other chars.
      uri = uri.replace('&', '&amp;')
      return uri

    def first( self):
      self.current = 0
      
    def last( self):
       self.current = len( self.stations)-1

    def play( self, the_sonos, index=-1):
#      self.current = index
#      print self.current
      description = self.name()
      description = description + ',' + self.icon()
      ui_out.log.info( ui_out.cmd_stream_start + ',' + description)
      result = self.play_current_preset( the_sonos)
      if result == True:
        ui_out.log.info( ui_out.cmd_stream_playing + ',' + description)
      else:
        ui_out.log.error( ui_out.cmd_stream_error + ',' + description)	
      return result

    def name( self):
       desc = self.stations[self.current]['title']
       return desc
       
    def icon( self):
      if self.icons:
		return self.icons.get_icon( self.current)

    def skip( self, the_sonos, direction):
      self.current += direction
      if self.current < 0:
        raise IndexError
      return self.play( the_sonos, self.current)


