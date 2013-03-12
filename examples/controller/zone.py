#!/usr/bin/env python

import sys

from soco import SoCo
from soco import SonosDiscovery
import ui_out




class SoHome(object):
    """ A container class for multiple Sonos Devices in a network
    """ 

    def __init__(self):
      self.whole_house = []
      sonos = SonosDiscovery()
      all_speakers = sonos.get_speaker_ips()
      for i in all_speakers:
          sonos = SoCo( i)
          result = sonos.get_speaker_info()
          self.whole_house.append(sonos)

    def __iter__(self):
      return iter(self.whole_house)
      
    def __getitem__(self, index):
        return self.whole_house[ index]

    def make_zone( self, master_name, *args):
      master = self.find(master_name)
      
      if master == None: 
        return(master)
        
      uid = master.get_speaker_info()['uid'] 
  
      # Try to connect the rest - ignore failures
      for arg in args:
        a_slave = self.find(arg)
        if a_slave:
            a_slave.join( uid)
       
      return( master)
      
    def make_zone_list( self, speaker_list):
      
      for idx, speaker in enumerate( speaker_list):
        if idx == 0:
          master = self.find(speaker)
          master.unjoin()
          uid = master.get_speaker_info()['uid'] 
        else:
          a_slave = self.find(speaker)
          if a_slave:
            a_slave.join( uid)
   
      return( master)
      
    """
    The uid is truncated to 24 characters as sometimes sonos requests appends it with other stuff which I don't know what it is.
    """ 
    def find(self, target):
      for speaker in self.whole_house:
        if speaker.speaker_info['zone_name'] == target or speaker.speaker_info['uid'][:24] == target[:24]:
           return speaker 

    def partymode(self):
      whole_house[0].partymode()
      return whole_house[0]
     
     
class SoGroup( SoHome):
  master = None
  slaves = []
    
    
  def __iter__(self):
    yield self.master
    for i in self.slaves:
      yield i
      
  def __getitem__(self, index):
    if index == 0: return self.master
    return self.slaves[ index - 1]
    
  def __str__(self):
    me = []
    for item in self:
       me.append( item.speaker_info['zone_name'])
    return ','.join( me)
        
  def modify_zone( self, speaker_list):
    candidates = []   
  
    for speaker in speaker_list:
      lookup = self.find(speaker)
      if lookup == None:
        print 'no such speaker ' + speaker
        return None
      else:
        candidates.append( lookup)
      
    if self.master == None:
      self.master = candidates[0]
      
    if self.master in candidates: 
      candidates.remove(self.master) 
    else:
      print 'oh oh remove group master todo'
    
    for remove in self.slaves:
      print 'check to remove ' + remove.speaker_info['zone_name']
      if not remove in candidates:
          remove.unjoin()
          self.slaves.remove( remove)

    uid = self.master.speaker_info['uid']
    for add in candidates:
      if not add in self.slaves:
        print 'add ' + add.speaker_info['zone_name']
        add.join( uid)
        self.slaves.append( add)
    
    ui_out.log.info( ui_out.cmd_group + ',' + str(self))
    
    return( self)
    
  def volume(self, target):
    for speaker in self:
      speaker.volume( target)
    ui_out.log.info( ui_out.cmd_volume + ',' + str(self) + ',' + str(target))
    
  def play_uri( self, uri_dict):
    description = uri_dict['name'] + ',' + uri_dict['icon']
    ui_out.log.info( ui_out.cmd_stream_start + ',' + description)
    result = self.master.play_uri( uri_dict['url'], uri_dict['meta'])
    if result == True:
      ui_out.log.info( ui_out.cmd_stream_playing + ',' + description)
    else:
      ui_out.log.error( ui_out.cmd_stream_error + ',' + description)    
    return result
     
     
  def get_current_track_info( self):
	result = self.master.get_current_track_info()
	return( result)
	  
          
  def get_queue( self):
	result = self.master.get_queue()
	return( result)

if __name__ == '__main__':
  zone = SoGroup()

  print 'Sonos Zone'  
  print zone.modify_zone( ['notexisting'])
  print zone.modify_zone( ['Living Room','notexisting'])
  print zone.modify_zone( ['Living Room'])
  print zone.modify_zone( ['Living Room','Kitchen'])
  final = zone.modify_zone( ['Living Room','Kitchen','Bedroom'])
  
  item = final.master.get_topology()
  item = final.master.get_topology()
  item = final.master.get_topology()
  if item['is_master']:
    standalone = ' (standalone)' if item['no_slaves'] == 0 else '' 
    print 'Group: "' +  item['group_name'] + '"' + standalone
    if item[ 'no_slaves'] > 0:
      split = item['all_uids'].split(',')
      for slave in split:
        lookup = zone.find( slave)
        print '--> ' + lookup.speaker_info['zone_name']
    else:
      lookup = zone.find( item['group_uid'])
      print 'I am slave: ' + lookup.speaker_info['zone_name'] + ' :('
      
    zone.volume(10)     
  

