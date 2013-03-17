import sonoscontroller, sys, logging
import ui_out

from soco import SoCo
from zone import SoGroup
from tunein import TuneIn



def please_wait():
  print 'LIGHTS wait'
	
def all_is_well():
  print 'LIGHTS normal'

def all_off():
  print 'LIGHTS Stop'

def update_active():
  print 'LIGHTS speakers'

class BlinkenLightsFilter(logging.Filter):
  
  controller=None
  
  def filter(self, rec):
	  
    if rec.levelno == logging.CRITICAL:
      print 'LIGHTS mental'
      return True
	  
    if ui_out.cmd_start in rec.msg:
      all_is_well()
      return True
      
    if ui_out.cmd_stop in rec.msg:
      all_off()
      return True

    if ui_out.cmd_group in rec.msg:
      update_active()
      return True
        
    if ui_out.cmd_stream_start in rec.msg:
      please_wait()
      return True
                    
    if ui_out.cmd_stream_start in rec.msg:
      all_is_well()
      return True
          
    return True		


enabled = False

if enabled:
    ui_out.log.addFilter(BlinkenLightsFilter())
    
