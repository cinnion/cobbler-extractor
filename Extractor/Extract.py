#!/usr/bin/env python3
'''
Extractor.Extract -- Extract cobbler configurations to shell scripts.

Extractor.Extract is a A utility to extract the distributions, profiles, systems, etc. to a batch of shell script commands.

It defines classes_and_methods

@author:     Douglas Needham

@copyright:  2018 Douglas Needham. All rights reserved.

@license:    TBD

@contact:    cinnion@gmail.com
@deffield    updated: Updated
'''

import sys
import os
import pprint as pp
from gettext import gettext as _, ngettext

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import SUPPRESS

env = os.getenv('PYTHONPATH')
from Extractor.Cobbler import Cobbler
from Extractor.Distro import Distros as Distros

__all__ = []
__version__ = 0.1
__date__ = '2018-05-01'
__updated__ = '2018-05-01'

DEBUG = 1
TESTRUN = 0
PROFILE = 0


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (
        program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Douglas Needham on %s.
  Copyright 2018 Douglas Needham. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(
            description=program_license, formatter_class=RawDescriptionHelpFormatter, add_help=False)
        parser.add_argument('--help', action='help', default=SUPPRESS,
                            help=_('show this help message and exit'))
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)
        parser.add_argument("-h", "--host", dest="host", default="cobbler.ka8zrt.com",
                            help="Hostname for the cobbler server [default: %(default)s]", metavar="hostname")
        parser.add_argument("-p", "--protocol", dest="protocol", choices=['http', 'https'], default="http",
                            help="Protocol for the XMLRPC connection [default: %(default)s]")
        parser.add_argument("-a", "--api", dest="api", default="cobbler_api",
                            help="API specifier [default: %(default)s]")

        # Process arguments
        args = parser.parse_args()

        cobbler = Cobbler(**vars(args))
        x = Distros(cobbler, hostname=args.host)
        print(x)

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    if DEBUG:
        pass
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'Extractor.Extract_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
