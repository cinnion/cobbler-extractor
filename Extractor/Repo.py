#!/usr/bin/env python3.6
'''
Created on May 25, 2018

@author: cinnion
'''

from Extractor.Cobbler import CobblerServer, CobblerRecord, KeywordMap
from shlex import quote
from operator import itemgetter, attrgetter
#import sys

__all__ = [
    'Repos',
    'Repo'
]
__version__ = 0.5
__date__ = '2018-05-25'
__updated__ = '2018-05-25'


class Repo(CobblerRecord):
    '''
    This is used to hold and output distributions.
    '''

    kw_map: KeywordMap = {
        'uid':                          ('uid', 'skip'),
        'ctime':                        ('ctime', 'timeStr'),
        'mtime':                        ('mtime', 'timeStr'),
        'depth':                        ('depth', 'skip'),
        'parent':                       ('parent', None),

        'arch':                         ('arch', None),
        'breed':                        ('breed', None),
        'comment':                      ('comment', None),
        'keep_updated':                 ('keep-updated', None),
        'mirror':                       ('mirror', None),
        'owners':                       ('owners', 'spaceList'),
        'rpm_list':                     ('rpm-list', None),
        'proxy':                        ('proxy', None),

        'apt_components':               ('apt-components', None),
        'apt_dists':                    ('apt-dists', None),
        'createrepo_flags':             ('createrepo-flags', None),
        'environment':                  ('environment', None),
        'mirror_locally':               ('mirror-locally', None),
        'priority':                     ('priority', None),
        'yumopts':                      ('yumopts', None),
    }

    def __init__(self, **kwargs):
        '''
        Constructor, taking parameters named following the CLI parameter names and setting an attribute with the value.
        '''
        self.name = kwargs.get('name')
        super().__init__(message='Unrecognized repo keyword: {} (Repo={})', **kwargs)


class Repos(CobblerServer):
    '''
    This is used to extract the distributions from cobbler and output them as cobbler CLI commands
    '''

    def __init__(self, server: CobblerServer, **kwargs):
        '''
        Constructor
        '''
        self.server = server

        self.repo_list = []

        repo_list = self.server.get_repos()
        for repo in repo_list:
            self.repo_list.append(self.create_repo(**repo))

        self.repo_list = sorted(self.repo_list, key=attrgetter('name'))
        self.loaded = True

    def __str__(self):
        cmds = []
        for repo in self.repo_list:
            cmds.append(str(repo))

        return('\n\n'.join(cmds) + '\n')

    def create_repo(self, **kwargs):
        r = Repo(**kwargs)
        return(r)


if __name__ == "__main__":
    x = Repos()
