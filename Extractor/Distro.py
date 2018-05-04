#!/usr/bin/env python3
'''
Created on Apr 29, 2018

@author: cinnion
'''

from Extractor.Cobbler import Cobbler
from shlex import quote
from operator import itemgetter, attrgetter

__all__ = [
    'Distros',
    'Distro'
]
__version__ = 0.1
__date__ = '2018-05-01'
__updated__ = '2018-05-01'


class Distro(object):
    '''
    This is used to hold and output distributions.
    '''

    kw_names = [
        'ctime',
        'mtime',
        'uid',
        'owners',
        'kernel',
        'initrd',
        'kopts',
        'kopts-post',
        'ksmeta',
        'arch',
        'breed',
        'os-version',
        'source-repos',
        'depth',
        'comment',
        'tree-build-time',
        'mgmt-classes',
        'boot-files',
        'fetchable-files',
        'template-files',
        'redhat-management-key',
        'redhat-management-server',
    ]

    def __init__(self, **kwargs):
        '''
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        '''
        self.name = kwargs.get('name')
        for kw in kwargs:
            if kw in self.kw_names:
                setattr(self, kw, kwargs[kw])

    def __repr__(self):
        args = []

        for kw in self.kw_names:
            if hasattr(self, kw):
                val = getattr(self, kw)
            else:
                val = None
            args[kw] = val

        return(args)

    def __str__(self):
        args = ['--name={}'.format(quote(self.name))]

        for kw in self.kw_names:
            if hasattr(self, kw):
                val = getattr(self, kw)
                if 'owners' == kw and len(val) > 0:
                    val = ' '.join(val)
                elif 'owners' == kw:
                    continue
                elif kw in ('ctime', 'mtime'):
                    val = str(val)
                elif 'uid' == kw:
                    continue
                elif 'depth' == kw:
                    continue
                elif 'comment' == kw and len(val) == 0:
                    continue

                arg = '--' + kw + '={}'.format(quote(val))
                args.append(arg)

        command = 'cobbler distro add ' + ' \\\n        '.join(args)

        return(command)


class Distros(object):
    '''
    This is used to extract the distributions from cobbler and output them as cobbler CLI commands
    '''

    def __init__(self, server, **kwargs):
        '''
        Constructor
        '''
        self.server = server

        self.distro_list = []

        distro_list = self.server.get_distros()
        for dist in distro_list:
            self.distro_list.append(self.create_distro(**dist))

        self.distro_list = sorted(self.distro_list, key=attrgetter('name'))
        self.loaded = True

    def __str__(self):
        cmds = []
        for dist in self.distro_list:
            cmds.append(str(dist))

        return('\n\n'.join(cmds))

    def create_distro(self, **dict):
        d = Distro(**dict)
        return(d)


if __name__ == "__main__":
    x = Distros()
