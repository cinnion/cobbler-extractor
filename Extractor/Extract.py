#!/usr/bin/env python3
"""
Extractor.Extract -- Extract cobbler configurations to shell scripts.

Extractor.Extract is a utility to extract the distributions, profiles, systems, etc. to a
batch of shell script commands.

It defines CLIError and main

@author:     Douglas Needham

@copyright:  2018-2024 Douglas Needham. All rights reserved.

@license:    BSD-3-Clause

@contact:    douglas.w.needham@gmail.com
"""

import sys
import os
import pprint as pp
from gettext import gettext as _, ngettext

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from argparse import SUPPRESS

from Cobbler import CobblerServer
from Repo import Repos
from Image import Images
from Distro import Distros
from MgmtClass import MgmtClasses
from Profile import Profiles
from System import Systems

__all__ = []
__version__ = 0.7
__date__ = '2018-05-01'
__updated__ = '2024-10-20'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

showAdds = False


class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):  # IGNORE:C0111
    """Command line options."""

    global showAdds

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
  Copyright 2018-2024 Douglas Needham. All rights reserved.

  Licensed under the 3-Clause BSD License
  https://opensource.org/license/bsd-3-clause

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    cleanupFormat = r'''
echo Cleaning up {0}s...
cobbler {0} list | xargs -I '<>' -n 1 cobbler {0} remove --name='<>' --recursive
'''

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
        parser.add_argument('-A', '--show-adds', dest="showAdds", action='store_true',
                            help='Display the progress by showing the first line of the cobbler add commands')
        parser.add_argument('-X', '--cleanup', dest='doCleanup', action='store_true',
                            help='Run a cleanup statement to delete all existing objects')

        # Process arguments
        args = parser.parse_args()

        if args.showAdds:
            showAdds = args.showAdds

        cobbler = CobblerServer(**vars(args))
        if args.doCleanup:
            print(cleanupFormat.format('mgmtclass'))
        x = MgmtClasses(cobbler, hostname=args.host)
        print(x)

        cobbler = CobblerServer(**vars(args))
        if args.doCleanup:
            print(cleanupFormat.format('image'))
        x = Images(cobbler, hostname=args.host)
        print(x)

        if args.doCleanup:
            print(cleanupFormat.format('repo'))
        x = Repos(cobbler, hostname=args.host)
        print(x)

        if args.doCleanup:
            print(cleanupFormat.format('distro'))
        x = Distros(cobbler, hostname=args.host)
        print(x)

        if args.doCleanup:
            print(cleanupFormat.format('profile'))
        x = Profiles(cobbler, hostname=args.host)
        print(x)

        if args.doCleanup:
            print(cleanupFormat.format('system'))
        x = Systems(cobbler, hostname=args.host)
        print(x)

        return 0
    except KeyboardInterrupt:
        # handle keyboard interrupt
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise e
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
