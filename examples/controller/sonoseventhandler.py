import sonoscontroller, sys, logging
import ui_out

from threading import Thread
from threading import Event
from threading import Lock

from soco import SoCo
from zone import SoGroup
from preset import Presets
from tunein import TuneIn
from queue import Queue
#from ui_out_gpio import BlinkenLightsFilter
from ui_out_screen import LcdFilter

user_wants_log_output = True;
speakers = [ 'Living Room', 'Kitchen', 'Bedroom', 'Dining Room' ]



class CommandFilter(logging.Filter):
  
  class Worker(Thread):
	  
    def __init__(self):
      Thread.__init__(self)
      self.trigger = Event()
      self.uri = None
      self.sonos = None
      self.daemon = True
      self.lock = Lock()

    def start_url(self, a_group, uri):
      with self.lock:
		self.sonos = a_group
		self.uri = uri
      self.trigger.set()

    
    def run(self):
      while True:
        self.trigger.wait()
        if self.sonos is None:
		  # take this as a sign to shut down gracefully
          break
        with self.lock:
          uri = self.uri
          self.uri = None
          self.trigger.clear()
        result = self.sonos.play_uri( uri)
        print result
           
  def __init__(self, daemon=False):
    if daemon:
      self.trigger = Event()
      self.thread = CommandFilter.Worker()
      self.thread.start()
     
  def filter(self, rec):
	  
    if sonoscontroller.cmd_on in rec.msg:
      ui_out.log.info( ui_out.cmd_start)
      return True
      
    if sonoscontroller.cmd_off in rec.msg:
      ui_out.log.info( ui_out.cmd_stop)
      return True

    if sonoscontroller.cmd_next in rec.msg:
      presets.skip( 1)
      return True

    if sonoscontroller.cmd_previous in rec.msg:
      presets.skip( -1)
      return True

    if sonoscontroller.cmd_group in rec.msg:
      args = rec.msg.split(",") 
      args.remove( sonoscontroller.cmd_group)
      self.master = the_group.modify_zone( args)
      return True
      
    if sonoscontroller.cmd_radio_preset in rec.msg:
      args = rec.msg.split(",") 
      args.remove( sonoscontroller.cmd_radio_preset)
      presets.goto( int(args[0]))
      uri = presets.get_preset()
      self.thread.start_url(the_group, uri )


      return True
 
    if sonoscontroller.cmd_stopall in rec.msg:	
      the_group.master.stop()
      return True
    
    if sonoscontroller.cmd_volume in rec.msg:
      args = rec.msg.split(',', 1) 
      ret = the_group.volume( int(args[1]))
      return True
          
    return True		

  def shutdown( self):
    if self.thread.isAlive():
      self.thread.start_url(None, None)
      self.thread.join()
  

the_group = SoGroup()
the_group.modify_zone(['Living Room'])




presets = Presets(the_group.master)
ti = TuneIn( the_group.master, 'tunein_icons')
q = Queue( the_group.master)
presets.add_preset_group( ti)
presets.add_preset_group( q)


if __name__ == '__main__':
  if user_wants_log_output:
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
   
    controller = CommandFilter( True)
    
    log = sonoscontroller.log
    log.addFilter(controller)
    
    ch.setFormatter(formatter)
    sonoscontroller.log.addHandler(ch)
    sonoscontroller.log.setLevel(logging.INFO)
    
#    ui_out.log.addFilter(BlinkenLightsFilter())
    ui_out.log.addFilter(LcdFilter())
    
    sonoscontroller.log.info( sonoscontroller.cmd_on)
    sonoscontroller.log.info( sonoscontroller.cmd_group + ",Living Room")
    sonoscontroller.log.info( sonoscontroller.cmd_volume + ",10")
    sonoscontroller.log.info( sonoscontroller.cmd_radio_preset + ",2")
    
    controller.shutdown()

    
    
    
#  sonoscontroller.SonosControl().run()

