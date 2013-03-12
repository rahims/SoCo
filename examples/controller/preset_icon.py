#!/usr/bin/env python

import inspect, os

class Preset_Icon(object):
    """ get icons.
    """ 
    image_dir    = 'icons'
    default_dir  = 'default'
    default_file = 'default'
    
    def __init__(self, directory):
      abs_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
      self.path = os.path.join( abs_path, self.image_dir )
      self.directory = directory
      if not os.path.exists(self.get_directory()):
        os.makedirs(self.get_directory())
      self.extension = '.png'
   
    def get_directory(self):
      return os.path.join( self.path, self.directory)

    def get_unique_icon( self, index):
      path = os.path.join( self.path, self.directory, str( index))
      path = path + self.extension
      if os.path.exists( path):
        return path

    def get_default_icon(self, index):
      path = os.path.join (self.path, self.default_dir, str( index)) + self.extension
      if os.path.exists( path):
        return( path)
      else:
		path = os.path.join (self.path, self.default_dir, self.default_file) + self.extension
		return path

    def get_icon(self, index):
      unique = self.get_unique_icon( index)
      if unique:
        return unique
      
      return self.get_default_icon( index)
		  


if __name__ == '__main__':


  tuneinicons = Preset_Icon('tunein')
  
  print tuneinicons.get_icon( 0)
  print tuneinicons.get_icon( 1)
  print tuneinicons.get_icon( 2)
  print tuneinicons.get_icon( 3)
  print tuneinicons.get_icon( 10)
  print tuneinicons.get_icon( 11)
