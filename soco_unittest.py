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
        self.method_name = 'volume'
        self.valid_values = range(101)

    def test_get(self):
        """ Test if the get functionality works and returns a valid value """
        volume = SOCO.volume()
        self.assertIn(volume, self.valid_values)

    def test_set(self):
        """ Tests if the set functionlity works when given valid arguments """
        volume = SOCO.volume()
        if volume < 100:
            new_volume = volume + 1
        else:
            new_volume = volume - 1
        self.assertIs(SOCO.volume(new_volume), True)
        self.assertEqual(SOCO.volume(), new_volume)
        SOCO.volume(volume)

    def test_invalid_arguments(self):
        """ Tests if the set functionality fails predictively when given
        invalid values
        """
        self.assertEqual(SOCO.volume(self.valid_values[0] - 1), 402)
        self.assertEqual(SOCO.volume(self.valid_values[-1] + 1), 402)

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
                        'for the zone to use for the unit tests')
    PARSER.add_argument('--list', action='store_const', const=True,
                        dest='zone_list', help='lists all the available zones'
                        ' and their IP addresses')
    PARSER.add_argument('--coverage', action='store_const', const=True,
                        help='unit test coverage statistics')
    ARGS = PARSER.parse_args()

    # Switch execution depending on command line input
    if ARGS.ip is not None:
        SOCO = soco.SoCo(ARGS.ip)
        # Delete command line arguments, otherwise unittest will complain
        sys.argv = sys.argv[:1]
        unittest.main()
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
        CLASSES  = []
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
