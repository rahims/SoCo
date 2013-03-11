
""" Example implementation of a plugin """


class ExamplePlugin(object):
    """ This file serves as an example of a SoCo plugin """

    def __init__(self, soco, arguments):
        """ We usually need a reference to the primary soco instanse, so we
        can leverage methods from it. Arguments are placed in a dictionary
        with all the special arguments this plugin needs.
        """
        self.soco = soco
        # E.g:
        self.user_name = arguments['user_name']

    def music_plugin_play(self):
        """ This is just a reimplementation of the ordinary play function, to
        show how we can use the general upnp methods from soco
        """
        response = self.soco.send_command(TRANSPORT_ENDPOINT,
            PLUGIN_PLAY_ACTION, PLUGIN_PLAY_BODY)

        if (response == PLUGIN_PLAY_RESPONSE):
            return True
        else:
            return self.soco.parse_error(response)

    def music_plugin_stop(self):
        """ This methods shows how, if we need it, we can use the soco
        functionality from inside the plugins
        """
        # Do magic plugin stuff before stopping
        print self.user_name
        # And then stop
        self.soco.stop()


TRANSPORT_ENDPOINT = '/MediaRenderer/AVTransport/Control'
PLUGIN_PLAY_ACTION = '"urn:schemas-upnp-org:service:AVTransport:1#Play"'
PLUGIN_PLAY_BODY = '''
<u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
  <InstanceID>0</InstanceID>
  <Speed>1</Speed>
</u:Play>
'''
PLUGIN_PLAY_RESPONSE = '''
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
 s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:PlayResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1">
    </u:PlayResponse>
  </s:Body>
</s:Envelope>'''
