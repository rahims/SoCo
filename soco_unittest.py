# -*- coding: utf-8 -*-
# pylint: disable-msg=R0904

""" This file contains the classes used to perform unit tests on the methods
in the SoCo class
"""

import sys
import soco
import inspect
import unittest
import argparse


class Volume(unittest.TestCase):
    """ Unit tests for the volume method """

    def setUp(self):  # pylint: disable-msg=C0103
        self.valid_values = range(101)

    def test_get_and_set(self):
        """ Tests if the set functionlity works when given valid arguments """
        old = SOCO.volume()
        self.assertIn(old, self.valid_values)
        if old == self.valid_values[0]:
            new = old + 1
        else:
            new = old - 1
        self.assertIs(SOCO.volume(new), True)
        self.assertEqual(SOCO.volume(), new)
        SOCO.volume(old)

    def test_invalid_arguments(self):
        """ Tests if the set functionality fails predictively when given
        invalid values
        """
        self.assertEqual(SOCO.volume(self.valid_values[0] - 1), 402)
        self.assertEqual(SOCO.volume(self.valid_values[-1] + 1), 402)


class Bass(unittest.TestCase):
    """ Unit tests for the bass method """

    def setUp(self):  # pylint: disable-msg=C0103
        self.valid_values = range(-10, 11)

    def test_get_and_set(self):
        """ Tests if the set functionlity works when given valid arguments """
        old = SOCO.bass()
        self.assertIn(old, self.valid_values)
        if old == self.valid_values[0]:
            new = old + 1
        else:
            new = old - 1
        self.assertIs(SOCO.bass(new), True)
        self.assertEqual(SOCO.bass(), new)
        SOCO.bass(old)

    def test_invalid_arguments(self):
        """ Tests if the set functionality produces the expected "coerce in
        range" functionality when given a value outside of its range
        """
        old = SOCO.bass()
        SOCO.bass(self.valid_values[0] - 1)
        self.assertEqual(SOCO.bass(), self.valid_values[0])
        SOCO.bass(self.valid_values[-1] + 1)
        self.assertEqual(SOCO.bass(), self.valid_values[-1])
        SOCO.bass(old)


class Treble(unittest.TestCase):
    """ Unit tests for the treble method """

    def setUp(self):  # pylint: disable-msg=C0103
        self.valid_values = range(-10, 11)

    def test_get_and_set(self):
        """ Tests if the set functionlity works when given valid arguments """
        old = SOCO.treble()
        self.assertIn(old, self.valid_values)
        if old == self.valid_values[0]:
            new = old + 1
        else:
            new = old - 1
        self.assertIs(SOCO.treble(new), True)
        self.assertEqual(SOCO.treble(), new)
        SOCO.treble(old)

    def test_invalid_arguments(self):
        """ Tests if the set functionality produces the expected "coerce in
        range" functionality when given a value outside its range
        """
        old = SOCO.treble()
        SOCO.treble(self.valid_values[0] - 1)
        self.assertEqual(SOCO.treble(), self.valid_values[0])
        SOCO.treble(self.valid_values[-1] + 1)
        self.assertEqual(SOCO.treble(), self.valid_values[-1])
        SOCO.treble(old)


class GetCurrentTrackInfo(unittest.TestCase):
    """ Unit test for the get_current_track_info method """

    def setUp(self):  # pylint: disable-msg=C0103
        # The value in this list must be kept up to date with the values in
        # the test_get doc string
        self.info_keys = ['album', 'artist', 'title', 'uri',
            'playlist_position', 'duration', 'album_art']

    def test_get(self):
        """ Test is the return value is a dictinary and contains the following
        keys: album, artist, title, uri, playlist_position, duration and
        album_art
        """
        info = SOCO.get_current_track_info()
        self.assertIsInstance(info, dict, 'Returned info is not a dict')
        self.assertEqual(info.keys(), self.info_keys,
            'Info does not contain the proper keys')


class AddToQueue(unittest.TestCase):
    """ Unit test for the add_to_queue method """

    ### TODO Finish implementation

    def test(self):
        """ Gets the current queue, adds the last item of the current queue
        and then compares the length of the old queue with the new and
        checks that the last two elements are identical
        """
        import time
        SOCO.pause()
        old_queue = SOCO.get_queue()
        self.assertTrue(len(old_queue) > 0,
            'Unit tests must be run with at least one item in the queue')
        # Add new element and check
        self.assertEqual(SOCO.add_to_queue(old_queue[-1]['uri']),
                         len(old_queue) + 1)
        new_queue = SOCO.get_queue()
        self.assertEqual(len(new_queue)-1, len(old_queue))
        self.assertEqual(new_queue[-1], new_queue[-2])
        # Clean up
        print time.time()
        SOCO.clear_queue()
        print time.time()
        for item in old_queue:
            SOCO.add_to_queue(item['uri'])
        print time.time()
        SOCO.play()
        print time.time()
        
        


class GetQueue(unittest.TestCase):
    """ Unit test for the get_queue method """

    def setUp(self):  # pylint: disable-msg=C0103
        # The value in this list must be kept up to date with the values in
        # the test_get doc string
        self.track_keys = ['album', 'artist', 'uri', 'album_art', 'title']

    def test_get(self):
        """ Tests is return value is a list of dictionaries and if each of
        the dictionaries contain the keys: album, artist, uri, album_art and
        title
        """
        queue = SOCO.get_queue()
        self.assertIsInstance(queue, list, 'Returned queue is not a list')
        self.assertTrue(len(queue) > 0,
            'Unit tests must be run with at least one item in the queue')
        for item in queue:
            self.assertIsInstance(item, dict, 'Item in queue is not a dict')
            self.assertEqual(item.keys(), self.track_keys,
                'Item in queue does not contain the proper keys')


if __name__ == "__main__":

    def get_ips_and_names():
        """ Return a list of zone ips and names """
        discovery = soco.SonosDiscovery()
        ips = discovery.get_speaker_ips()
        names = [soco.SoCo(ip).get_speaker_info()['zone_name'] for ip in ips]
        return zip(ips, names)

    # Build argument parser
    DESCRIPTION = ('Unit tests for SoCo.\n\nIn order to be able to control '
        'which zone the unit tests are\nperformed on, an IP address must be '
        'provided. For a list of all\npossible IP adresses use the --list '
        'argument.\n\nExamples: python soco_unittest.py --ip 192.168.0.110\n'
        '          python soco_unittest.py --list')
    PARSER = argparse.ArgumentParser(description=DESCRIPTION,
                            formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument('--ip', type=str, default=None, help='the IP address '
                        'for the zone to be used for the unit tests')
    PARSER.add_argument('--list', action='store_const', const=True,
                        dest='zone_list', help='lists all the available zones'
                        ' and their IP addresses')
    PARSER.add_argument('--coverage', action='store_const', const=True,
                        help='unit test coverage statistics')
    PARSER.add_argument('--verbose', type=int, default=1, help='Verbosity '
                        'level for the unit tests (1 or 2). 1 is default.')
    ARGS = PARSER.parse_args()

    # Switch execution depending on command line input
    if ARGS.ip is not None:
        SOCO = soco.SoCo(ARGS.ip)
        # Delete command line arguments, otherwise unittest will complain
        sys.argv = sys.argv[:1]
        SUITE = unittest.TestLoader().loadTestsFromModule(
            sys.modules[__name__])
        unittest.TextTestRunner(verbosity=ARGS.verbose).run(SUITE)
    elif ARGS.zone_list:
        PATTERN = '{0}\t{1}\n'
        NAMES_AND_IPS = get_ips_and_names()
        sys.stdout.write(PATTERN.format('IP', 'Name'))
        for items in NAMES_AND_IPS:
            sys.stdout.write(PATTERN.format(items[0],
                                            items[1].encode('utf-8')))
    elif ARGS.coverage:
        # Get all but 'private' methods from soco
        METHODS = []
        for name, obj in inspect.getmembers(soco.SoCo,
                                            predicate=inspect.ismethod):
            if name[0] != '_':
                METHODS.append(name.replace('_', ''))

        # Get all classes in this module
        CLASSES = []
        for name, obj in inspect.getmembers(sys.modules[__name__],
                                            predicate=inspect.isclass):
            CLASSES.append(name.lower())

        sys.stdout.write('\n')
        for method in METHODS:
            if method in CLASSES:
                sys.stdout.write(method.ljust(26, '.') + 'COVERED\n')
            else:
                sys.stdout.write(method.ljust(26, '.') + 'NOT COVERED\n')
        PERCENTAGE = float(len(CLASSES)) / len(METHODS) * 100
        sys.stdout.write('\n\n{0:.2f}% methods covered\n'.format(PERCENTAGE))
    else:
        PARSER.print_help()
