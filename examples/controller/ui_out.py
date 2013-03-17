import sys, logging


log = logging.getLogger("SonosUserFeedback")

activated = True

cmd_start = 'start_ui'
cmd_stop = 'stop_ui'

cmd_stream_start = 'cmd_stream_start'
cmd_stream_playing = 'cmd_stream_done'
cmd_stream_error = 'cmd_stream_error'

cmd_group = 'cmd_group'
cmd_group_error = 'cmd_group_error'

cmd_navigate = 'cmd_navigate'

cmd_group = 'cmd_group'
cmd_joined = 'cmd_joined'
cmd_left = 'cmd_left'

cmd_volume ='cmd_volume'

if activated:
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
   
#    log = uout_log.log
#    log.addFilter(CommandFilter())
    
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(logging.INFO)




