#!/usr/bin/env python3
"""
Created on Oct 20, 2024

@author:     Douglas Needham

@copyright:  2018-2024 Douglas Needham. All rights reserved.

@license:    BSD-3-Clause

@contact:    douglas.w.needham@gmail.com
"""

from operator import attrgetter
from pprint import pp

from Extractor.Cobbler import CobblerServer, CobblerRecord, KeywordMap

__all__ = [
    'MgmtClasses',
    'MgmtClass'
]
__version__ = 0.5
__date__ = '2024-10-20'
__updated__ = '2024-10-20'


class MgmtClass(CobblerRecord):
    """
    This is used to hold and output management classes.
    """

    kw_map: KeywordMap = {
        'uid': ('uid', 'skip'),
        'ctime': ('ctime', 'skip'),
        'mtime': ('mtime', 'skip'),
        'depth': ('depth', 'skip'),

        'owners': ('owners', 'spaceList'),
        'class_name': ('class-name', None),
        'is_definition': ('is-definition', None),
        'files': ('files', None),
        'packages': ('packages', None),
        'params': ('params', None),

        'comment': ('comment', None),
    }

    def __init__(self, **kwargs):
        """
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        """
        self.name = kwargs.get('name')
        super().__init__('Unrecognized mgmtclass keyword: {} (mgmtclass={})', **kwargs)


class MgmtClasses(CobblerServer):
    """
    This is used to extract the management classes from cobbler and output them as cobbler CLI commands
    """

    def __init__(self, server: CobblerServer, **_kwargs):
        """
        Constructor
        """
        self.server = server

        self.mgmtclass_list = []

        mgmtclass_list = self.server.get_mgmtclasses()
        for mgmtclass in mgmtclass_list:
            self.mgmtclass_list.append(self.create_mgmtclass(**mgmtclass))

        self.mgmtclass_list = sorted(
            self.mgmtclass_list, key=attrgetter('name'))
        self.loaded = True

    def __str__(self):
        cmds = []
        for mgmtclass in self.mgmtclass_list:
            cmds.append(str(mgmtclass))

        return '\n\n'.join(cmds) + '\n'

    @staticmethod
    def create_mgmtclass(**kwargs):
        p = MgmtClass(**kwargs)
        return p


if __name__ == "__main__":
    if __name__ == "__main__":
        s = CobblerServer('foo')
        pp(MgmtClasses(s))
