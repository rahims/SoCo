# producer
import logging

log = logging.getLogger("SonosControl") 

class SonosControl(object):
    def run(self):
		        
        log.info( cmd_on)
        log.info( cmd_group + ",Living Room,Kitchen")
        log.info( cmd_radio_preset + ",2")
#       log.info( cmd_next)
#       log.info( cmd_previous)
#       log.info( cmd_previous)
        
        
        log.info( cmd_volume + ",10")
        log.info( cmd_volume + ",11")
        log.info( cmd_volume + ",12")
        log.info( cmd_volume + ",13")
        log.info( cmd_volume + ",14")
        log.info( cmd_group + ",Living Room,Bedroom,Kitchen")
        log.info( cmd_group + ",Living Room,Kitchen")
#        log.info( cmd_stopall)
        log.info( cmd_off)


cmd_on = "<on>"
cmd_off = "<off>"
cmd_next = "<next>"
cmd_previous = "<previous>"
cmd_group = "<group>"
cmd_radio_preset="<preset>"
cmd_stopall="<stop>"
cmd_volume="<volume>"
cmd_add_speaker="<add>"


      
