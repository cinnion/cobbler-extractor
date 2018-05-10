#!/usr/bin/env python3
'''
Created on Apr 29, 2018

@author: cinnion
'''

from Extractor.Cobbler import CobblerServer, CobblerRecord
from shlex import quote
from operator import itemgetter, attrgetter
#import sys

__all__ = [
    'Distros',
    'Distro'
]
__version__ = 0.1
__date__ = '2018-05-01'
__updated__ = '2018-05-01'


class Distro(CobblerRecord):
    '''
    This is used to hold and output distributions.
    '''

    kw_map = {
        'ctime': 'ctime',
        'mtime': 'mtime',
        'uid': 'uid',
        'owners': 'owners',
        'kernel': 'kernel',
        'initrd': 'initrd',
        'kernel_options': 'kopts',
        'kernel_options_post': 'kopts-post',
        'ks_meta': 'ksmeta',
        'arch': 'arch',
        'breed': 'breed',
        'os_version': 'os-version',
        'source_repos': 'source-repos',
        'depth': 'depth',
        'comment': 'comment',
        'tree_build_time': 'tree-build-time',
        'mgmt_classes': 'mgmt-classes',
        'boot_files': 'boot-files',
        'fetchable_files': 'fetchable-files',
        'template_files': 'template-files',
        'redhat_management_key': 'redhat-management-key',
        'redhat_management_server': 'redhat-management-server',
    }

    def __init__(self, **kwargs):
        '''
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        '''
        self.name = kwargs.get('name')
        super().__init__(message='Unrecognized distro keyword: {} (Distro={})', **kwargs)

    def __str__(self):
        args = ['--name={}'.format(quote(self.name))]

        mapped_args = super().__str__()
        args.append(mapped_args)

        command = 'cobbler distro add ' + ' \\\n        '.join(args)

        return(command)


class Distros(object):
    '''
    This is used to extract the distributions from cobbler and output them as cobbler CLI commands
    '''

    def __init__(self, server: CobblerServer, **kwargs):
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

    def create_distro(self, **kwargs):
        d = Distro(**kwargs)
        return(d)


if __name__ == "__main__":
    x = Distros()
